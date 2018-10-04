import pytest

from models import ApiErrors, PcObject
from models.venue import TooManyVirtualVenuesException
from tests.conftest import clean_database
from utils.test_utils import create_offerer, create_venue, create_thing_offer, create_event_offer


@clean_database
@pytest.mark.standalone
def test_offerer_cannot_have_address_and_isVirtual(app):
    # Given
    offerer = create_offerer('123456789', '1 rue Test', 'Test city', '93000', 'Test offerer')
    PcObject.check_and_save(offerer)

    venue = create_venue(offerer, name='Venue_name', booking_email='booking@email.com', is_virtual=True)
    venue.address = '1 test address'

    # When
    with pytest.raises(ApiErrors):
        PcObject.check_and_save(venue)


@clean_database
@pytest.mark.standalone
def test_offerer_not_isVirtual_cannot_have_null_address(app):
    # Given
    offerer = create_offerer('123456789', '1 rue Test', 'Test city', '93000', 'Test offerer')
    PcObject.check_and_save(offerer)

    venue = create_venue(offerer, name='Venue_name', booking_email='booking@email.com', address=None, postal_code=None,
                         city=None, departement_code=None, is_virtual=False)

    # When
    with pytest.raises(ApiErrors):
        PcObject.check_and_save(venue)


@clean_database
@pytest.mark.standalone
def test_offerer_cannot_create_a_second_virtual_venue(app):
    # Given
    offerer = create_offerer('123456789', '1 rue Test', 'Test city', '93000', 'Test offerer')
    PcObject.check_and_save(offerer)

    venue = create_venue(offerer, name='Venue_name', booking_email='booking@email.com', address=None, postal_code=None,
                         city=None, departement_code=None, is_virtual=True)
    PcObject.check_and_save(venue)

    new_venue = create_venue(offerer, name='Venue_name', booking_email='booking@email.com', address=None,
                             postal_code=None, city=None, departement_code=None, is_virtual=True)

    # When
    with pytest.raises(TooManyVirtualVenuesException):
        PcObject.check_and_save(new_venue)


@clean_database
@pytest.mark.standalone
def test_offerer_cannot_update_a_second_venue_to_be_virtual(app):
    # Given
    offerer = create_offerer('123456789', '1 rue Test', 'Test city', '93000', 'Test offerer')
    PcObject.check_and_save(offerer)

    venue = create_venue(offerer, address=None, postal_code=None, city=None, departement_code=None, is_virtual=True)
    PcObject.check_and_save(venue)

    new_venue = create_venue(offerer, is_virtual=False)
    PcObject.check_and_save(new_venue)

    # When
    new_venue.isVirtual = True
    new_venue.postalCode = None
    new_venue.address = None
    new_venue.city = None
    new_venue.departementCode = None

    # Then
    with pytest.raises(TooManyVirtualVenuesException):
        PcObject.check_and_save(new_venue)


@pytest.mark.standalone
@clean_database
def test_nOffers(app):
    offerer = create_offerer()
    venue = create_venue(offerer)
    offer_1 = create_thing_offer(venue)
    offer_2 = create_event_offer(venue)
    offer_4 = create_event_offer(venue)
    offer_5 = create_thing_offer(venue)
    PcObject.check_and_save(offer_1, offer_2, offer_4, offer_5)

    # when
    n_offers = venue.nOffers

    # then
    assert n_offers == 4