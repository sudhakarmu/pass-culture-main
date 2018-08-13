from unittest.mock import Mock

import pytest

from domain.offer import check_digital_offer_consistency, InconsistentOffer
from models import Offer, Venue, Thing

find_thing = Mock()

offer = Offer()
offer.thingId = 20


@pytest.mark.standalone
def test_check_digital_offer_consistency_raises_an_error_for_physical_venue_and_digital_thing():
    # given
    venue = Venue(from_dict={'isVirtual': False})
    find_thing.return_value = Thing(from_dict={'url': 'https://zerlngzergner.fr'})

    # when
    with pytest.raises(InconsistentOffer) as e:
        check_digital_offer_consistency(offer, venue, find_thing=find_thing)

    # then
    assert str(e.value) == 'Offer.venue is not virtual but Offer.thing has an URL'


@pytest.mark.standalone
def test_check_digital_offer_consistency_does_not_raise_an_error_for_virtual_venue_and_digital_thing():
    # given
    venue = Venue(from_dict={'isVirtual': True})
    find_thing.return_value = Thing(from_dict={'url': 'https://zerlngzergner.fr'})

    # when
    result = check_digital_offer_consistency(offer, venue, find_thing=find_thing)

    # then
    assert result is None


@pytest.mark.standalone
def test_check_digital_offer_consistency_raises_an_error_for_virtual_venue_and_physical_thing():
    # given
    venue = Venue(from_dict={'isVirtual': True})
    find_thing.return_value = Thing(from_dict={'url': None})

    # when
    with pytest.raises(InconsistentOffer) as e:
        check_digital_offer_consistency(offer, venue, find_thing=find_thing)

    # then
    assert str(e.value) == 'Offer.venue is virtual but Offer.thing does not have an URL'


@pytest.mark.standalone
def test_check_digital_offer_consistency_does_not_raise_an_error_for_physical_venue_and_physical_thing():
    # given
    venue = Venue(from_dict={'isVirtual': False})
    find_thing.return_value = Thing(from_dict={'url': None})

    # when
    result = check_digital_offer_consistency(offer, venue, find_thing=find_thing)

    # then
    assert result is None
