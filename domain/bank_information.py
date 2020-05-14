from typing import List

from models import BankInformation, Venue, Offerer
from models.bank_information import BankInformationStatus


status_weight = {
    BankInformationStatus.ACCEPTED: 2,
    BankInformationStatus.DRAFT: 1,
    BankInformationStatus.REJECTED: 0
}


def new_application_can_update_bank_information(bank_information: BankInformation,
                                                new_application_id: int,
                                                new_application_status: int):
    same_demarches_simplifiees_application = new_application_id == bank_information.applicationId

    new_status_is_more_advanced_than_previous = (
        status_weight[new_application_status] >= status_weight[bank_information.status])

    return same_demarches_simplifiees_application or new_status_is_more_advanced_than_previous


class CannotRegisterBankInformation(Exception):
    pass


def check_offerer_presence(offerer: Offerer):
    if not offerer:
        raise CannotRegisterBankInformation("Offerer not found")


def check_venue_presence(venue: Venue):
    if not venue:
        raise CannotRegisterBankInformation("Venue not found")


def check_venue_queried_by_name(venues: List[Venue]):
    if len(venues) == 0:
        raise CannotRegisterBankInformation("Venue name not found")
    if len(venues) > 1:
        raise CannotRegisterBankInformation("Multiple venues found")


def check_new_bank_information_older_than_saved_one(bank_information: BankInformation, application_details):
    is_new_bank_information_older_than_saved_one = bank_information.dateModifiedAtLastProvider is not None and application_details.modification_date < bank_information.dateModifiedAtLastProvider
    if is_new_bank_information_older_than_saved_one:
        raise CannotRegisterBankInformation(
            'Received application details are older than saved one')


def check_new_bank_information_has_a_more_advanced_status(bank_information: BankInformation, application_details):
    is_new_bank_information_status_more_important_than_saved_one = bank_information.status and status_weight[
        application_details.status] < status_weight[bank_information.status]
    if is_new_bank_information_status_more_important_than_saved_one:
        raise CannotRegisterBankInformation(
            'Received application details state does not allow to change bank information')
