import re
from urllib.parse import urlencode

from pcapi import settings
from pcapi.core.bookings.models import Booking
from pcapi.core.educational.models import CollectiveOffer
from pcapi.core.educational.models import CollectiveOfferTemplate
from pcapi.core.offerers import models as offerers_models
from pcapi.core.offers.models import Offer
from pcapi.core.users import models as users_models
from pcapi.utils.human_ids import humanize


def generate_firebase_dynamic_link(path: str, params: dict | None) -> str:
    universal_link_url = f"{settings.WEBAPP_V2_URL}/{path}"
    if params:
        universal_link_url = universal_link_url + f"?{urlencode(params)}"

    firebase_dynamic_query_string = urlencode({"link": universal_link_url})
    return f"{settings.FIREBASE_DYNAMIC_LINKS_URL}/?{firebase_dynamic_query_string}"


def offer_app_link(offer_id: int, utm: str | None = None) -> str:
    base = f"{settings.WEBAPP_V2_URL}/offer/{offer_id}"
    if utm:
        return f"{base}?{utm}"
    return base


def booking_app_link(booking: Booking) -> str:
    return f"{settings.WEBAPP_V2_URL}/reservation/{booking.id}/details"


def build_pc_pro_offer_link(offer: CollectiveOffer | CollectiveOfferTemplate | Offer) -> str:
    if isinstance(offer, CollectiveOffer):
        return f"{settings.PRO_URL}/offre/{humanize(offer.id)}/collectif/edition"

    if isinstance(offer, CollectiveOfferTemplate):
        return f"{settings.PRO_URL}/offre/T-{humanize(offer.id)}/collectif/edition"

    return f"{settings.PRO_URL}/offre/individuelle/{humanize(offer.id)}/recapitulatif"


def build_pc_pro_offerer_link(offerer: offerers_models.Offerer) -> str:
    return f"{settings.PRO_URL}/accueil?structure={humanize(offerer.id)}"


def build_pc_pro_venue_link(venue: offerers_models.Venue) -> str:
    if venue.isVirtual:
        return build_pc_pro_offerer_link(venue.managingOfferer)
    return f"{settings.PRO_URL}/structures/{humanize(venue.managingOffererId)}/lieux/{humanize(venue.id)}"


def build_pc_pro_venue_bookings_link(venue: offerers_models.Venue) -> str:
    return f"{settings.PRO_URL}/reservations?offerVenueId={humanize(venue.id)}"


def build_pc_pro_venue_offers_link(venue: offerers_models.Venue) -> str:
    return f"{settings.PRO_URL}/offres?lieu={humanize(venue.id)}"


def build_pc_pro_user_email_validation_link(user: users_models.User) -> str:
    return f"{settings.PRO_URL}/inscription/validation/{user.validationToken}"


def build_backoffice_public_account_link(user_id: int) -> str:
    return f"{settings.BACKOFFICE_URL}/public-accounts/{user_id}"


def substitute_id_by_url_public_account(found_id: str) -> str:
    return f'<a class="link-primary" href="{build_backoffice_public_account_link(int(found_id))}" target="_blank">{found_id}</a>'


def build_backoffice_public_account_link_in_comment(comment: str) -> str:
    return re.sub(r"(\d+)$", lambda m: substitute_id_by_url_public_account(m.group(1)), comment)
