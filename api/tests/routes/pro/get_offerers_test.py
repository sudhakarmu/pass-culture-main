import pytest

from pcapi.core.offers import factories as offers_factories
from pcapi.core.users import factories as users_factories
from pcapi.model_creators.generic_creators import create_offerer
from pcapi.model_creators.generic_creators import create_user_offerer
from pcapi.repository import repository
from pcapi.utils.human_ids import dehumanize


class Returns200Test:
    @pytest.mark.usefixtures("db_session")
    def when_logged_in_and_return_an_offerer_with_one_managed_venue(self, client):
        # given
        offerer1 = offers_factories.OffererFactory(siren="123456781", name="offreur C", id=1)
        venue = offers_factories.VenueFactory(managingOfferer=offerer1)
        repository.save(offerer1, venue)

        pro = users_factories.ProFactory(offerers=[offerer1])

        # when
        response = client.with_session_auth(pro.email).get("/offerers")

        # then
        assert response.status_code == 200
        offerer_response = response.json[0]
        managed_venues_response = offerer_response["managedVenues"][0]
        assert "validationToken" not in managed_venues_response
        assert dehumanize(offerer_response["id"]) == 1

    @pytest.mark.usefixtures("db_session")
    def when_logged_in_and_return_a_list_of_offerers_sorted_alphabetically(self, client):
        # given
        offerer1 = offers_factories.OffererFactory(siren="123456781", name="offreur C")
        offerer2 = offers_factories.OffererFactory(siren="123456782", name="offreur A")
        offerer3 = offers_factories.OffererFactory(siren="123456783", name="offreur B")
        repository.save(offerer1, offerer3, offerer2)

        pro = users_factories.ProFactory(offerers=[offerer1, offerer2, offerer3])
        repository.save(pro)

        # when
        response = client.with_session_auth(pro.email).get("/offerers")

        # then
        assert response.status_code == 200
        offerers = response.json
        assert len(offerers) == 3
        names = [offerer["name"] for offerer in offerers]
        assert names == ["offreur A", "offreur B", "offreur C"]

    @pytest.mark.usefixtures("db_session")
    def when_logged_in_and_return_a_list_of_offerers_including_non_validated_structures(self, client):
        # given
        pro = users_factories.ProFactory()
        offerer1 = offers_factories.OffererFactory(siren="123456781", name="offreur A")
        offerer2 = offers_factories.OffererFactory(siren="123456782", name="offreur B")
        offerer3 = offers_factories.OffererFactory(siren="123456783", name="offreur C")
        user_offerer1 = offers_factories.UserOffererFactory(user=pro, offerer=offerer1, validationToken=None)
        user_offerer2 = offers_factories.UserOffererFactory(user=pro, offerer=offerer2, validationToken="AZE123")
        user_offerer3 = offers_factories.UserOffererFactory(user=pro, offerer=offerer3, validationToken=None)
        repository.save(user_offerer1, user_offerer2, user_offerer3)

        # when
        response = client.with_session_auth(pro.email).get("/offerers")

        # then
        assert response.status_code == 200
        offerers = response.json
        assert len(offerers) == 3
        names = [offerer["name"] for offerer in offerers]
        assert names == ["offreur A", "offreur B", "offreur C"]

        assert offerers[0]["userHasAccess"] is True
        assert offerers[1]["userHasAccess"] is False
        assert offerers[2]["userHasAccess"] is True

    @pytest.mark.usefixtures("db_session")
    def when_current_user_is_not_admin_and_returns_only_offers_managed_by_him(self, client):
        # given
        offerer1 = offers_factories.OffererFactory(siren="123456781", name="offreur C")
        offerer2 = offers_factories.OffererFactory(siren="123456782", name="offreur A")
        offerer3 = offers_factories.OffererFactory(siren="123456783", name="offreur B")
        repository.save(offerer1, offerer3, offerer2)

        pro = users_factories.ProFactory(offerers=[offerer1, offerer2])

        # when
        response = client.with_session_auth(pro.email).get("/offerers")

        # then
        assert response.status_code == 200
        assert len(response.json) == 2

    @pytest.mark.usefixtures("db_session")
    def when_current_user_is_admin_and_returns_all_offerers(self, client):
        # given
        offerer1 = offers_factories.OffererFactory(siren="123456781", name="offreur C")
        offerer2 = offers_factories.OffererFactory(siren="123456782", name="offreur A")
        offerer3 = offers_factories.OffererFactory(siren="123456783", name="offreur B")
        repository.save(offerer1, offerer3, offerer2)

        user = users_factories.AdminFactory(offerers=[offerer1, offerer2])

        # when
        response = client.with_session_auth(user.email).get("/offerers")

        # then
        assert response.status_code == 200
        assert len(response.json) == 3

    @pytest.mark.usefixtures("db_session")
    def when_user_is_admin_and_param_validated_is_false_and_returns_all_info_of_all_offerers(self, client):
        # given
        offerer1 = create_offerer(siren="123456781", name="offreur A", validation_token="F1TVYSGV")
        offerer2 = create_offerer(siren="123456782", name="offreur B")
        offers_factories.BankInformationFactory(offerer=offerer1)
        offers_factories.BankInformationFactory(offerer=offerer2)

        user = users_factories.AdminFactory(offerers=[offerer1, offerer2])

        # when
        response = client.with_session_auth(user.email).get("/offerers?validated=false")

        # then
        assert response.status_code == 200
        assert len(response.json) == 1
        offerer_response = response.json[0]
        assert offerer_response["name"] == "offreur A"
        assert set(offerer_response.keys()) == {
            "address",
            "bic",
            "city",
            "dateCreated",
            "dateModifiedAtLastProvider",
            "demarchesSimplifieesApplicationId",
            "fieldsUpdated",
            "iban",
            "id",
            "idAtProviders",
            "isActive",
            "isValidated",
            "dateValidated",
            "lastProviderId",
            "managedVenues",
            "nOffers",
            "name",
            "postalCode",
            "siren",
            "thumbCount",
            "userHasAccess",
        }

    @pytest.mark.usefixtures("db_session")
    def when_user_is_admin_and_param_validated_is_true_and_returns_only_validated_offerer(self, client):
        # given
        offerer1 = create_offerer(siren="123456781", name="offreur C", validation_token=None)
        offerer2 = create_offerer(siren="123456782", name="offreur A", validation_token="AFYDAA")
        offers_factories.BankInformationFactory(applicationId=1, offerer=offerer1)
        offers_factories.BankInformationFactory(applicationId=2, offerer=offerer2)

        user = users_factories.AdminFactory(offerers=[offerer1, offerer2])

        # when
        response = client.with_session_auth(user.email).get("/offerers?validated=true")

        # then
        assert response.status_code == 200
        assert len(response.json) == 1
        offerer_response = response.json[0]
        assert offerer_response["name"] == "offreur C"

    @pytest.mark.usefixtures("db_session")
    def when_param_validated_is_false_and_returns_only_not_validated_offerers(self, client):
        # given
        pro = users_factories.ProFactory()
        offerer1 = offers_factories.OffererFactory(siren="123456781", name="offreur C", validationToken=None)
        offerer2 = offers_factories.OffererFactory(siren="123456782", name="offreur A", validationToken="AZE123")
        offerer3 = offers_factories.OffererFactory(siren="123456783", name="offreur B", validationToken=None)
        user_offerer1 = offers_factories.UserOffererFactory(user=pro, offerer=offerer1)
        user_offerer2 = offers_factories.UserOffererFactory(user=pro, offerer=offerer2)
        user_offerer3 = offers_factories.UserOffererFactory(user=pro, offerer=offerer3)
        repository.save(user_offerer1, user_offerer2, user_offerer3)

        # when
        response = client.with_session_auth(pro.email).get("/offerers?validated=false")

        # then
        assert response.status_code == 200
        assert len(response.json) == 1

    @pytest.mark.usefixtures("db_session")
    def when_param_validated_is_true_and_returns_only_validated_offerers(self, client):
        # given
        pro = users_factories.ProFactory()
        offerer1 = offers_factories.OffererFactory(siren="123456781", name="offreur C", validationToken=None)
        offerer2 = offers_factories.OffererFactory(siren="123456782", name="offreur A", validationToken="AZE123")
        offerer3 = offers_factories.OffererFactory(siren="123456783", name="offreur B", validationToken=None)
        user_offerer1 = offers_factories.UserOffererFactory(user=pro, offerer=offerer1)
        user_offerer2 = offers_factories.UserOffererFactory(user=pro, offerer=offerer2)
        user_offerer3 = offers_factories.UserOffererFactory(user=pro, offerer=offerer3)
        repository.save(user_offerer1, user_offerer2, user_offerer3)

        # when
        response = client.with_session_auth(pro.email).get("/offerers?validated=true")

        # then
        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json[0]["name"] == "offreur B"
        assert response.json[1]["name"] == "offreur C"

    @pytest.mark.usefixtures("db_session")
    def when_param_validated_is_true_returns_all_info_of_validated_offerers(self, client):
        # given
        pro = users_factories.ProFactory()
        offerer1 = create_offerer(siren="123456781", name="offreur C", validation_token=None)
        offerer2 = create_offerer(siren="123456782", name="offreur A", validation_token="AZE123")
        offerer3 = create_offerer(siren="123456783", name="offreur B", validation_token=None)
        user_offerer1 = create_user_offerer(pro, offerer1)
        user_offerer2 = create_user_offerer(pro, offerer2)
        user_offerer3 = create_user_offerer(pro, offerer3)
        offers_factories.BankInformationFactory(offerer=offerer1)
        offers_factories.BankInformationFactory(offerer=offerer2)
        offers_factories.BankInformationFactory(offerer=offerer3)
        repository.save(user_offerer1, user_offerer2, user_offerer3)

        # when
        response = client.with_session_auth(pro.email).get("/offerers?validated=true")

        # then
        assert response.status_code == 200
        assert len(response.json) == 2
        assert set(response.json[0].keys()) == set(
            [
                "address",
                "bic",
                "city",
                "dateCreated",
                "dateModifiedAtLastProvider",
                "dateValidated",
                "demarchesSimplifieesApplicationId",
                "fieldsUpdated",
                "iban",
                "id",
                "idAtProviders",
                "isActive",
                "isValidated",
                "lastProviderId",
                "managedVenues",
                "nOffers",
                "name",
                "postalCode",
                "siren",
                "thumbCount",
                "userHasAccess",
            ]
        )

    @pytest.mark.usefixtures("db_session")
    def when_no_bank_information_for_offerer(self, client):
        # given
        pro = users_factories.ProFactory()
        offerer1 = offers_factories.OffererFactory(siren="123456781", name="offreur C")
        user_offerer1 = offers_factories.UserOffererFactory(user=pro, offerer=offerer1)
        repository.save(user_offerer1)

        # when
        response = client.with_session_auth(pro.email).get("/offerers?validated=true")

        # then
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["bic"] is None
        assert response.json[0]["iban"] is None

    @pytest.mark.usefixtures("db_session")
    def test_returns_metadata(self, client):
        # given
        pro = users_factories.ProFactory(email="user@test.com")
        offerer = offers_factories.OffererFactory(name="offreur C")
        user_offerer = offers_factories.UserOffererFactory(user=pro, offerer=offerer)
        repository.save(user_offerer)
        auth_request = client.with_session_auth(email="user@test.com")

        # when
        response = auth_request.get("/offerers")

        # then
        assert response.status_code == 200
        assert response.headers["Total-Data-Count"] == "1"

    @pytest.mark.usefixtures("db_session")
    def test_returns_proper_data_count_by_counting_distinct_offererss(self, client):
        # given
        pro = users_factories.ProFactory(email="user@test.com")
        offerer1 = offers_factories.OffererFactory(name="offreur", siren="123456789")
        user_offerer1 = offers_factories.UserOffererFactory(user=pro, offerer=offerer1)
        offerer2 = offers_factories.OffererFactory(name="offreur 2", siren="123456781")
        user_offerer2 = offers_factories.UserOffererFactory(user=pro, offerer=offerer2)
        venue1 = offers_factories.VenueFactory(managingOfferer=offerer1)
        venue2 = offers_factories.VenueFactory(siret="12345678912346", managingOfferer=offerer1)
        repository.save(user_offerer1, user_offerer2, venue1, venue2)

        # when
        response = client.with_session_auth(email="user@test.com").get("/offerers")

        # then
        assert response.status_code == 200
        assert response.headers["Total-Data-Count"] == "2"

    @pytest.mark.usefixtures("db_session")
    def test_returns_only_active_offerers(self, client):
        # given
        pro_user = users_factories.ProFactory(email="user@test.com")
        active_offerer = offers_factories.OffererFactory(name="active_offerer", siren="1", isActive=True)
        active_user_offerer = offers_factories.UserOffererFactory(user=pro_user, offerer=active_offerer)
        inactive_offerer = offers_factories.OffererFactory(name="inactive_offerer", siren="2", isActive=False)
        inactive_user_offerer = offers_factories.UserOffererFactory(user=pro_user, offerer=inactive_offerer)
        repository.save(active_user_offerer, inactive_user_offerer)

        # when
        request = client.with_session_auth(email=pro_user.email)
        response = request.get("/offerers?is_active=true")

        # then
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["name"] == active_offerer.name


class Returns400Test:
    @pytest.mark.usefixtures("db_session")
    def when_param_validated_is_not_true_nor_false(self, client):
        # given
        offerer1 = offers_factories.OffererFactory(siren="123456781", name="offreur C")
        offerer2 = offers_factories.OffererFactory(siren="123456782", name="offreur A")
        offerer3 = offers_factories.OffererFactory(siren="123456783", name="offreur B")
        repository.save(offerer1, offerer3, offerer2)

        user = users_factories.AdminFactory(offerers=[offerer1, offerer2])

        # when
        response = client.with_session_auth(user.email).get("/offerers?validated=blabla")

        # then
        assert response.status_code == 400
        assert response.json["validated"] == ["Le paramètre 'validated' doit être 'true' ou 'false'"]
