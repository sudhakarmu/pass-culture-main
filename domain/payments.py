import csv
import itertools
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from hashlib import sha256
from io import BytesIO, StringIO
from typing import List, Dict
from uuid import UUID

from flask import render_template
from lxml import etree

from domain.reimbursement import BookingReimbursement
from models import PaymentTransaction
from models.payment import Payment, PaymentDetails
from models.payment_status import TransactionStatus
from models.user import WalletBalance
from repository.booking_queries import find_date_used

XML_NAMESPACE = {'ns': 'urn:iso:std:iso:20022:tech:xsd:pain.001.001.03'}


class InvalidTransactionXML(Exception):
    pass


class Transaction:
    def __init__(self, creditor_iban: str, creditor_bic: str, creditor_name: str, creditor_siren: str,
                 end_to_end_id: UUID, amount: Decimal, custom_message: str):
        self.creditor_iban = creditor_iban
        self.creditor_bic = creditor_bic
        self.creditor_name = creditor_name
        self.creditor_siren = creditor_siren
        self.end_to_end_id = end_to_end_id
        self.amount = amount
        self.custom_message = custom_message


def create_payment_for_booking(booking_reimbursement: BookingReimbursement) -> Payment:
    payment = Payment()
    payment.booking = booking_reimbursement.booking
    payment.amount = booking_reimbursement.reimbursed_amount
    payment.reimbursementRule = booking_reimbursement.reimbursement.value.description
    payment.reimbursementRate = booking_reimbursement.reimbursement.value.rate
    payment.author = 'batch'
    payment.customMessage = make_custom_message(datetime.utcnow())
    venue = booking_reimbursement.booking.stock.resolvedOffer.venue

    if venue.iban:
        payment.iban = venue.iban
        payment.bic = venue.bic
    else:
        offerer = venue.managingOfferer
        payment.iban = offerer.iban
        payment.bic = offerer.bic

    payment.recipientName = venue.managingOfferer.name
    payment.recipientSiren = venue.managingOfferer.siren

    if payment.iban:
        payment.setStatus(TransactionStatus.PENDING)
    else:
        payment.setStatus(TransactionStatus.NOT_PROCESSABLE, detail='IBAN et BIC manquants sur l\'offreur')

    return payment


def filter_out_already_paid_for_bookings(booking_reimbursements: List[BookingReimbursement]) -> List[
    BookingReimbursement]:
    return list(filter(lambda x: not x.booking.payments, booking_reimbursements))


def generate_transaction_file(payments: List[Payment], pass_culture_iban: str, pass_culture_bic: str, message_id: str,
                              remittance_code: str) -> str:
    transactions = _group_payments_into_transactions(payments)
    total_amount = sum([transaction.amount for transaction in transactions])
    now = datetime.utcnow()

    return render_template(
        'transactions/transaction_banque_de_france.xml',
        message_id=message_id,
        creation_datetime=now.isoformat(),
        requested_execution_datetime=datetime.strftime(now + timedelta(days=7), "%Y-%m-%d"),
        transactions=transactions,
        number_of_transactions=len(transactions),
        total_amount=total_amount,
        pass_culture_iban=pass_culture_iban,
        pass_culture_bic=pass_culture_bic,
        initiating_party_id=remittance_code,
    )


def validate_transaction_file_structure(transaction_file: str) -> str:
    xsd = render_template('transactions/transaction_banque_de_france.xsd')
    xsd_doc = etree.parse(BytesIO(xsd.encode()))
    xsd_schema = etree.XMLSchema(xsd_doc)

    encoded_file = transaction_file.encode('utf-8')
    xml = BytesIO(encoded_file)
    xml_doc = etree.parse(xml)

    xsd_schema.assertValid(xml_doc)


def generate_file_checksum(file: str):
    encoded_file = file.encode('utf-8')
    return sha256(encoded_file).digest()


def create_all_payments_details(payments: List[Payment], find_booking_date_used=find_date_used) -> List[PaymentDetails]:
    return list(map(lambda p: create_payment_details(p, find_booking_date_used), payments))


def create_payment_details(payment: Payment, find_booking_date_used=find_date_used) -> PaymentDetails:
    return PaymentDetails(payment, find_booking_date_used(payment.booking))


def generate_payment_details_csv(payments_details: List[PaymentDetails]) -> str:
    output = StringIO()
    csv_lines = [details.as_csv_row() for details in payments_details]
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(PaymentDetails.CSV_HEADER)
    writer.writerows(csv_lines)
    return output.getvalue()


def generate_wallet_balances_csv(wallet_balances: List[WalletBalance]) -> str:
    output = StringIO()
    csv_lines = [balance.as_csv_row() for balance in wallet_balances]
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(WalletBalance.CSV_HEADER)
    writer.writerows(csv_lines)
    return output.getvalue()


def make_custom_message(date: datetime.date) -> str:
    month_and_year = date.strftime('%m-%Y')
    period = '1ère' if date.day < 15 else '2nde'
    return 'pass Culture Pro - remboursement %s quinzaine %s' % (period, month_and_year)


def generate_payment_transaction(message_id: str, checksum: str, payments: List[Payment]) -> PaymentTransaction:
    payment_transaction = PaymentTransaction()
    payment_transaction.messageId = message_id
    payment_transaction.checksum = checksum
    payment_transaction.payments = payments
    return payment_transaction


def read_message_id_in_transaction_file(xml_file: str) -> str:
    xml = BytesIO(xml_file.encode())
    tree = etree.parse(xml, etree.XMLParser())
    node = tree.find('//ns:GrpHdr/ns:MsgId', namespaces=XML_NAMESPACE)
    return node.text


def group_payments_by_status(payments: List[Payment]) -> Dict:
    groups = {}
    for p in payments:
        status_name = p.currentStatus.status.name

        if status_name in groups:
            groups[status_name].append(p)
        else:
            groups[status_name] = [p]
    return groups


def _group_payments_into_transactions(payments: List[Payment]) -> List[Transaction]:
    payments_with_iban = sorted(filter(lambda x: x.iban, payments), key=lambda x: (x.iban, x.bic))
    payments_by_iban = itertools.groupby(payments_with_iban, lambda x: (x.iban, x.bic))

    transactions = []
    for (iban, bic), grouped_payments in payments_by_iban:
        payments_of_iban = list(grouped_payments)
        amount = sum([payment.amount for payment in payments_of_iban])
        end_to_end_id = uuid.uuid4()

        for payment in payments_of_iban:
            payment.transactionEndToEndId = end_to_end_id

        transactions.append(
            Transaction(iban, bic, payments_of_iban[0].recipientName, payments_of_iban[0].recipientSiren, end_to_end_id,
                        amount, payments_of_iban[0].customMessage))
    return transactions
