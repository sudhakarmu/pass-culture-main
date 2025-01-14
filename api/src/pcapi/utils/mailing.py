from datetime import datetime
import logging
from pprint import pformat

from flask import render_template

from pcapi import settings
from pcapi.connectors import sirene
from pcapi.core.bookings.models import Booking
from pcapi.core.educational.models import CollectiveBooking
from pcapi.core.educational.models import CollectiveOffer
from pcapi.core.educational.models import CollectiveOfferTemplate
from pcapi.core.educational.models import CollectiveStock
import pcapi.core.mails.models as mails_models
import pcapi.core.offerers.models as offerers_models
from pcapi.core.offers.models import Offer
from pcapi.core.offers.models import Stock
from pcapi.core.offers.utils import offer_app_link
from pcapi.utils import urls
from pcapi.utils.date import utc_datetime_to_department_timezone
from pcapi.utils.human_ids import humanize
import pcapi.utils.postal_code as postal_code_utils


logger = logging.getLogger(__name__)


def build_pc_pro_create_password_link(token_value: str) -> str:
    return f"{settings.PRO_URL}/creation-de-mot-de-passe/{token_value}"


def build_pc_pro_reset_password_link(token_value: str) -> str:
    return f"{settings.PRO_URL}/mot-de-passe-perdu?token={token_value}"


def build_pc_webapp_reset_password_link(token_value: str) -> str:
    return f"{settings.WEBAPP_V2_URL}/mot-de-passe-perdu?token={token_value}"


def format_booking_date_for_email(booking: Booking | CollectiveBooking) -> str:
    if isinstance(booking, CollectiveBooking) or booking.stock.offer.isEvent:
        stock = booking.collectiveStock if isinstance(booking, CollectiveBooking) else booking.stock
        date_in_tz = get_event_datetime(stock)  # type: ignore [arg-type]
        offer_date = date_in_tz.strftime("%d-%b-%Y")
        return offer_date
    return ""


def format_booking_hours_for_email(booking: Booking | CollectiveBooking) -> str:
    if isinstance(booking, CollectiveBooking) or booking.stock.offer.isEvent:
        stock = booking.collectiveStock if isinstance(booking, CollectiveBooking) else booking.stock
        date_in_tz = get_event_datetime(stock)  # type: ignore [arg-type]
        event_hour = date_in_tz.hour
        event_minute = date_in_tz.minute
        return f"{event_hour}h" if event_minute == 0 else f"{event_hour}h{event_minute}"
    return ""


def make_offerer_internal_validation_email(
    offerer: offerers_models.Offerer,
    user_offerer: offerers_models.UserOfferer,
    siren_info: sirene.SirenInfo | None,
) -> mails_models.TransactionalWithoutTemplateEmailData:
    offerer_departement_code = postal_code_utils.PostalCode(offerer.postalCode).get_departement_code()

    email_html = render_template(
        "mails/internal_validation_email.html",
        user_offerer=user_offerer,
        offerer=offerer,
        offerer_pro_link=urls.build_pc_pro_offerer_link(offerer),
        offerer_summary=pformat(_summarize_offerer_vars(offerer, siren_info)),
        user_summary=pformat(_summarize_user_vars(user_offerer)),
        api_entreprise=pformat(siren_info.dict() if siren_info else None),
        api_url=settings.API_URL,
    )

    return mails_models.TransactionalWithoutTemplateEmailData(
        subject="%s - inscription / rattachement PRO à valider : %s" % (offerer_departement_code, offerer.name),
        html_content=email_html,
        sender=mails_models.TransactionalSender.SUPPORT_PRO,
    )


def make_offer_creation_notification_email(
    offer: Offer | CollectiveOffer | CollectiveOfferTemplate,
) -> mails_models.TransactionalWithoutTemplateEmailData:
    author = getattr(offer, "author", None) or offer.venue.managingOfferer.first_user
    venue = offer.venue
    pro_link_to_offer = urls.build_pc_pro_offer_link(offer)
    pro_venue_link = f"{settings.PRO_URL}/structures/{humanize(venue.managingOffererId)}/lieux/{humanize(venue.id)}"
    webapp_link_to_offer = offer_app_link(offer)
    html = render_template(
        "mails/offer_creation_notification_email.html",
        offer=offer,
        venue=venue,
        author=author,
        pro_link_to_offer=pro_link_to_offer,
        webapp_link_to_offer=webapp_link_to_offer,
        pro_venue_link=pro_venue_link,
    )
    location_information = offer.venue.departementCode or "numérique"
    is_educational_offer_label = "EAC " if offer.isEducational else ""

    return mails_models.TransactionalWithoutTemplateEmailData(
        subject=f"[Création d’offre {is_educational_offer_label}- {location_information}] {offer.name}",
        html_content=html,
        sender=mails_models.TransactionalSender.SUPPORT_PRO,
    )


def make_offer_rejection_notification_email(
    offer: Offer | CollectiveOfferTemplate | CollectiveOffer,
) -> mails_models.TransactionalWithoutTemplateEmailData:
    author = getattr(offer, "author", None) or offer.venue.managingOfferer.first_user
    pro_link_to_offer = urls.build_pc_pro_offer_link(offer)
    venue = offer.venue
    pro_venue_link = f"{settings.PRO_URL}/structures/{humanize(venue.managingOffererId)}/lieux/{humanize(venue.id)}"
    html = render_template(
        "mails/offer_creation_refusal_notification_email.html",
        offer=offer,
        venue=venue,
        author=author,
        pro_link_to_offer=pro_link_to_offer,
        pro_venue_link=pro_venue_link,
    )
    location_information = offer.venue.departementCode or "numérique"
    is_educational_offer_label = "" if isinstance(offer, Offer) else "EAC "

    return mails_models.TransactionalWithoutTemplateEmailData(
        subject=f"[Création d’offre {is_educational_offer_label}: refus - {location_information}] {offer.name}",
        html_content=html,
        sender=mails_models.TransactionalSender.SUPPORT_PRO,
    )


def get_event_datetime(stock: CollectiveStock | Stock) -> datetime:
    if isinstance(stock, Stock):
        departement_code = stock.offer.venue.departementCode
    else:
        departement_code = stock.collectiveOffer.venue.departementCode
    if departement_code is not None:
        date_in_utc = stock.beginningDatetime
        date_in_tz = utc_datetime_to_department_timezone(date_in_utc, departement_code)
    else:
        date_in_tz = stock.beginningDatetime  # type: ignore [assignment]

    return date_in_tz


def make_suspended_fraudulent_beneficiary_by_ids_notification_email(
    fraudulent_users: dict, nb_cancelled_bookings: int
) -> mails_models.TransactionalWithoutTemplateEmailData:
    html = render_template(
        "mails/suspend_fraudulent_beneficiary_by_ids_notification_email.html",
        fraudulent_users=fraudulent_users,
        nb_cancelled_bookings=nb_cancelled_bookings,
        nb_fraud_users=len(fraudulent_users),
    )

    return mails_models.TransactionalWithoutTemplateEmailData(
        subject="Fraude : suspension des utilisateurs frauduleux par ids",
        html_content=html,
        sender=mails_models.TransactionalSender.SUPPORT_PRO,
    )


def _summarize_offerer_vars(
    offerer: offerers_models.Offerer,
    siren_info: sirene.SirenInfo | None,
) -> dict:
    if siren_info:
        head_office_siret = siren_info.head_office_siret
        ape_code = siren_info.ape_code
    else:
        head_office_siret = ape_code = "Inconnu (erreur API Sirene)"
    return {
        "name": offerer.name,
        "siren": offerer.siren,
        "address": offerer.address,
        "city": offerer.city,
        "postalCode": offerer.postalCode,
        "siret": head_office_siret,
        "legal_main_activity": ape_code,
    }


def _summarize_user_vars(user_offerer: offerers_models.UserOfferer) -> dict:
    return {
        "firstName": user_offerer.user.firstName,
        "lastName": user_offerer.user.lastName,
        "email": user_offerer.user.email,
        "phoneNumber": user_offerer.user.phoneNumber,
        "activity": user_offerer.user.activity,
    }
