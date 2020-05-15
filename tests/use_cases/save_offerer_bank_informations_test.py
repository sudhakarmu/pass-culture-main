from unittest.mock import patch
from datetime import datetime

import pytest
from use_cases.save_offerer_bank_informations import SaveOffererBankInformations
from models import ApiErrors

from models.bank_information import BankInformationStatus
from tests.model_creators.generic_creators import create_bank_information, create_offerer
from tests.connector_creators.demarches_simplifiees_creators import \
    offerer_demarche_simplifiee_application_detail_response
from repository import repository
from tests.conftest import clean_database
from models import BankInformation
from domain.bank_information import CannotRegisterBankInformation


@patch('domain.demarches_simplifiees.get_application_details')
class SaveOffererBankInformationsTest:
    def setup_method(self):
        self.save_offerer_bank_informations = SaveOffererBankInformations()

    @clean_database
    def test_when_dms_state_is_refused_should_create_the_correct_bank_information(self, mock_application_details,
                                                                                  app):
        # Given
        application_id = '8'
        offerer = create_offerer(siren='793875030')
        repository.save(offerer)
        mock_application_details.return_value = offerer_demarche_simplifiee_application_detail_response(
            siren="793875030", bic="SOGEFRPP", iban="FR7630007000111234567890144", idx=8, state='refused')

        # When
        self.save_offerer_bank_informations.execute(application_id=application_id)

        # Then
        bank_information_count = BankInformation.query.count()
        assert bank_information_count == 1
        bank_information = BankInformation.query.one()
        assert bank_information.bic is None
        assert bank_information.iban is None
        assert bank_information.status == BankInformationStatus.REJECTED

    @clean_database
    def test_when_dms_state_is_without_continuation_should_create_the_correct_bank_information(self,
                                                                                               mock_application_details,
                                                                                               app):
        # Given
        application_id = '8'
        offerer = create_offerer(siren='793875030')
        repository.save(offerer)
        mock_application_details.return_value = offerer_demarche_simplifiee_application_detail_response(
            siren="793875030", bic="SOGEFRPP", iban="FR7630007000111234567890144", idx=8,
            state='without_continuation')

        # When
        self.save_offerer_bank_informations.execute(application_id=application_id)

        # Then
        bank_information_count = BankInformation.query.count()
        assert bank_information_count == 1
        bank_information = BankInformation.query.one()
        assert bank_information.bic is None
        assert bank_information.iban is None
        assert bank_information.status == BankInformationStatus.REJECTED

    @clean_database
    def test_when_dms_state_is_closed_should_create_the_correct_bank_information(self, mock_application_details,
                                                                                 app):
        # Given
        application_id = '8'
        offerer = create_offerer(siren='793875030')
        repository.save(offerer)
        mock_application_details.return_value = offerer_demarche_simplifiee_application_detail_response(
            siren="793875030", bic="SOGEFRPP", iban="FR7630007000111234567890144", idx=8, state='closed')

        # When
        self.save_offerer_bank_informations.execute(application_id=application_id)

        # Then
        bank_information_count = BankInformation.query.count()
        assert bank_information_count == 1
        bank_information = BankInformation.query.one()
        assert bank_information.bic == "SOGEFRPP"
        assert bank_information.iban == "FR7630007000111234567890144"
        assert bank_information.status == BankInformationStatus.ACCEPTED

    @clean_database
    def test_when_dms_state_is_received_should_create_the_correct_bank_information(self, mock_application_details,
                                                                                   app):
        # Given
        application_id = '8'
        offerer = create_offerer(siren='793875030')
        repository.save(offerer)
        mock_application_details.return_value = offerer_demarche_simplifiee_application_detail_response(
            siren="793875030", bic="SOGEFRPP", iban="FR7630007000111234567890144", idx=8, state='received')

        # When
        self.save_offerer_bank_informations.execute(application_id=application_id)

        # Then
        bank_information_count = BankInformation.query.count()
        assert bank_information_count == 1
        bank_information = BankInformation.query.one()
        assert bank_information.bic is None
        assert bank_information.iban is None
        assert bank_information.status == BankInformationStatus.DRAFT

    @clean_database
    def test_when_dms_state_is_initiated_should_create_the_correct_bank_information(self, mock_application_details,
                                                                                    app):
        # Given
        application_id = '8'
        offerer = create_offerer(siren='793875030')
        repository.save(offerer)
        mock_application_details.return_value = offerer_demarche_simplifiee_application_detail_response(
            siren="793875030", bic="SOGEFRPP", iban="FR7630007000111234567890144", idx=8, state='initiated')

        # When
        self.save_offerer_bank_informations.execute(application_id=application_id)

        # Then
        bank_information_count = BankInformation.query.count()
        assert bank_information_count == 1
        bank_information = BankInformation.query.one()
        assert bank_information.bic is None
        assert bank_information.iban is None
        assert bank_information.status == BankInformationStatus.DRAFT

    @clean_database
    def test_when_no_offerer_siren_specified_should_not_create_bank_information(self, mock_application_details,
                                                                                app):
        # Given
        application_id = '8'
        mock_application_details.return_value = offerer_demarche_simplifiee_application_detail_response(
            siren="793875030", bic="SOGEFRPP", iban="FR7630007000111234567890144", idx=8)

        # When
        with pytest.raises(CannotRegisterBankInformation) as error:
            self.save_offerer_bank_informations.execute(application_id=application_id)

        # Then
        bank_information_count = BankInformation.query.count()
        assert bank_information_count == 0
        assert error.value.args == (f'Offerer not found',)

    @clean_database
    def test_when_state_is_unknown(self, mock_application_details, app):
        # Given
        application_id = '8'
        offerer = create_offerer(siren='793875030')
        repository.save(offerer)
        unknown_status = 'unknown_status'
        mock_application_details.return_value = offerer_demarche_simplifiee_application_detail_response(
            siren="793875030", bic="SOGEFRPP", iban="FR7630007000111234567890144", idx=8, state=unknown_status)

        # When
        with pytest.raises(CannotRegisterBankInformation) as error:
            self.save_offerer_bank_informations.execute(application_id=application_id)

        # Then
        bank_information_count = BankInformation.query.count()
        assert bank_information_count == 0
        assert error.value.args == (
            f'Unknown Demarches Simplifiées state {unknown_status}',)

    # UpdateBankInformationByApplicationIdTest
    @clean_database
    def test_when_rib_and_offerer_change_everything_should_be_updated(self, mock_application_details, app):
        # Given
        application_id = '8'
        offerer = create_offerer(siren='793875030')
        new_offerer = create_offerer(siren='793875019')
        bank_information = create_bank_information(
            application_id=8,
            bic='QSDFGH8Z555',
            iban="NL36INGB2682297498",
            offerer=offerer,
        )
        repository.save(offerer, new_offerer, bank_information)
        mock_application_details.return_value = offerer_demarche_simplifiee_application_detail_response(
            siren="793875019", bic="SOGEFRPP", iban="FR7630007000111234567890144", idx=8)

        # When
        self.save_offerer_bank_informations.execute(application_id=application_id)

        # Then
        bank_information_count = BankInformation.query.count()
        assert bank_information_count == 1
        bank_information = BankInformation.query.one()
        assert bank_information.bic == 'SOGEFRPP'
        assert bank_information.iban == 'FR7630007000111234567890144'
        assert bank_information.offererId == new_offerer.id

    @clean_database
    def test_when_status_change_rib_should_be_correctly_updated(self, mock_application_details, app):
        # Given
        application_id = '8'
        offerer = create_offerer(siren='793875030')
        bank_information = create_bank_information(
            application_id=8,
            bic='QSDFGH8Z555',
            iban="NL36INGB2682297498",
            offerer=offerer,
            status=BankInformationStatus.ACCEPTED
        )
        repository.save(offerer, bank_information)
        mock_application_details.return_value = offerer_demarche_simplifiee_application_detail_response(
            siren="793875030", bic="QSDFGH8Z555", iban="NL36INGB2682297498", idx=8, state="initiated")

        # When
        self.save_offerer_bank_informations.execute(application_id=application_id)

        # Then
        bank_information_count = BankInformation.query.count()
        assert bank_information_count == 1
        bank_information = BankInformation.query.one()
        assert bank_information.bic == None
        assert bank_information.iban == None
        assert bank_information.status == BankInformationStatus.DRAFT

    @clean_database
    def test_when_overriding_another_bank_information_should_raise(self, mock_application_details, app):
        # Given
        application_id = '8'
        offerer = create_offerer(siren='793875030')
        other_offerer = create_offerer(siren='793875019')
        bank_information = create_bank_information(
            application_id=8,
            bic='QSDFGH8Z555',
            iban="NL36INGB2682297498",
            offerer=offerer,
        )
        other_bank_information = create_bank_information(
            application_id=79,
            bic='QSDFGH8Z555',
            iban="NL36INGB2682297498",
            offerer=other_offerer,
        )
        repository.save(offerer, other_offerer,
                        bank_information, other_bank_information)
        mock_application_details.return_value = offerer_demarche_simplifiee_application_detail_response(
            siren="793875019", bic="QSDFGH8Z555", iban="NL36INGB2682297498", idx=8)

        # When
        with pytest.raises(ApiErrors) as errors:
            self.save_offerer_bank_informations.execute(application_id=application_id)

        # Then
        bank_information_count = BankInformation.query.count()
        assert bank_information_count == 2
        assert errors.value.errors['"offererId"'] == [
            'Une entrée avec cet identifiant existe déjà dans notre base de données']

    # OverrideBankInformationByReffererTest
    @clean_database
    def test_when_receive_new_closed_application_should_override_previous_one(self, mock_application_details, app):
        # Given
        application_id = '8'
        offerer = create_offerer(siren='793875030')
        bank_information = create_bank_information(
            application_id=79,
            bic='QSDFGH8Z555',
            iban="NL36INGB2682297498",
            offerer=offerer,
            date_modified_at_last_provider=datetime(2018, 1, 1)
        )
        repository.save(offerer, bank_information)
        mock_application_details.return_value = offerer_demarche_simplifiee_application_detail_response(
            siren="793875030", bic="SOGEFRPP", iban="FR7630007000111234567890144", idx=8)

        # When
        self.save_offerer_bank_informations.execute(application_id=application_id)

        # Then
        bank_information_count = BankInformation.query.count()
        assert bank_information_count == 1
        bank_information = BankInformation.query.one()
        assert bank_information.bic == 'SOGEFRPP'
        assert bank_information.iban == 'FR7630007000111234567890144'
        assert bank_information.applicationId == 8

    @clean_database
    def test_when_receive_new_application_with_draft_state_should_update_previously_rejected_bank_information(self,
                                                                                                              mock_application_details,
                                                                                                              app):
        # Given
        application_id = '8'
        offerer = create_offerer(siren='793875030')
        bank_information = create_bank_information(
            application_id=79,
            bic=None,
            iban=None,
            offerer=offerer,
            date_modified_at_last_provider=datetime(2018, 1, 1),
            status=BankInformationStatus.REJECTED
        )
        repository.save(offerer, bank_information)
        mock_application_details.return_value = offerer_demarche_simplifiee_application_detail_response(
            siren="793875030", bic="SOGEFRPP", iban="FR7630007000111234567890144", idx=8, state="initiated")

        # When
        self.save_offerer_bank_informations.execute(application_id=application_id)

        # Then
        bank_information_count = BankInformation.query.count()
        assert bank_information_count == 1
        bank_information = BankInformation.query.one()
        assert bank_information.bic == None
        assert bank_information.iban == None
        assert bank_information.status == BankInformationStatus.DRAFT

    @clean_database
    def test_when_receive_new_application_with_lower_status_should_reject(self, mock_application_details, app):
        # Given
        application_id = '8'
        offerer = create_offerer(siren='793875030')
        bank_information = create_bank_information(
            application_id=79,
            bic='QSDFGH8Z555',
            iban="NL36INGB2682297498",
            offerer=offerer,
            date_modified_at_last_provider=datetime(2018, 1, 1),
            status=BankInformationStatus.ACCEPTED
        )
        repository.save(offerer, bank_information)
        mock_application_details.return_value = offerer_demarche_simplifiee_application_detail_response(
            siren="793875030", bic="SOGEFRPP", iban="FR7630007000111234567890144", idx=8, state="initiated")

        # When
        with pytest.raises(CannotRegisterBankInformation) as error:
            self.save_offerer_bank_informations.execute(application_id=application_id)

        # Then
        bank_information_count = BankInformation.query.count()
        assert bank_information_count == 1
        bank_information = BankInformation.query.one()
        assert bank_information.bic == 'QSDFGH8Z555'
        assert bank_information.iban == "NL36INGB2682297498"
        assert bank_information.status == BankInformationStatus.ACCEPTED
        assert bank_information.applicationId == 79
        assert error.value.args == (
            f'Received application details state does not allow to change bank information',)

    @clean_database
    def test_when_receive_older_application_should_reject(self, mock_application_details, app):
        # Given
        application_id = '8'
        offerer = create_offerer(siren='793875030')
        bank_information = create_bank_information(
            application_id=79,
            bic='QSDFGH8Z555',
            iban="NL36INGB2682297498",
            offerer=offerer,
            date_modified_at_last_provider=datetime(2020, 1, 1)
        )
        repository.save(offerer, bank_information)
        mock_application_details.return_value = offerer_demarche_simplifiee_application_detail_response(
            siren="793875030", bic="SOGEFRPP", iban="FR7630007000111234567890144", idx=8)

        # When
        with pytest.raises(CannotRegisterBankInformation) as error:
            self.save_offerer_bank_informations.execute(application_id=application_id)

        # Then
        bank_information_count = BankInformation.query.count()
        assert bank_information_count == 1
        bank_information = BankInformation.query.one()
        assert bank_information.bic == 'QSDFGH8Z555'
        assert bank_information.iban == "NL36INGB2682297498"
        assert bank_information.status == BankInformationStatus.ACCEPTED
        assert bank_information.applicationId == 79
        assert error.value.args == (
            f'Received application details are older than saved one',)
