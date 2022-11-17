import datetime

from dateutil.relativedelta import relativedelta
import pytest

import pcapi.core.fraud.factories as fraud_factories
import pcapi.core.fraud.models as fraud_models
from pcapi.core.mails.transactional.users.ubble_ko_reminder import find_users_that_failed_ubble_check_seven_days_ago
import pcapi.core.users.factories as users_factories
import pcapi.core.users.models as users_models


def build_user_with_ko_retryable_ubble_fraud_check(
    user: users_models.User | None = None,
    user_age: int = 18,
    ubble_date_created: datetime.datetime = datetime.datetime.utcnow() - relativedelta(days=7),
    ubble_eligibility: users_models.EligibilityType = users_models.EligibilityType.AGE18,
    # pylint: disable=dangerous-default-value
    reasonCodes: list[fraud_models.FraudReasonCode] = [fraud_models.FraudReasonCode.ID_CHECK_NOT_AUTHENTIC],
) -> users_models.User:
    """
    Generates a user and a fraud check with a retryable ubble status
    By default, the user is 18 years old and the fraud check is 7 days old
    If a user is provided, it will be used instead of generating a new one
    """
    if user is None:
        user = users_factories.UserFactory(
            dateOfBirth=datetime.datetime.utcnow() - relativedelta(years=user_age),
        )
    fraud_factories.BeneficiaryFraudCheckFactory(
        user=user,
        type=fraud_models.FraudCheckType.UBBLE,
        status=fraud_models.FraudCheckStatus.KO,
        reasonCodes=reasonCodes,
        dateCreated=ubble_date_created,
        eligibilityType=ubble_eligibility,
    )
    return user


@pytest.mark.usefixtures("db_session")
class FindUsersThatFailedUbbleTest:
    def setup_method(self):
        self.eighteen_years_ago = datetime.datetime.utcnow() - relativedelta(years=18)

    def should_find_users_that_failed_ubble_check_seven_days_ago(self):
        # Given
        user = build_user_with_ko_retryable_ubble_fraud_check()

        # When
        users = find_users_that_failed_ubble_check_seven_days_ago()

        # Then
        assert users == [user]

    def should_not_find_users_that_failed_ubble_check_six_days_ago(self):
        # Given
        build_user_with_ko_retryable_ubble_fraud_check(
            ubble_date_created=datetime.datetime.utcnow() - relativedelta(days=6)
        )

        # When
        users = find_users_that_failed_ubble_check_seven_days_ago()

        # Then
        assert users == []

    def should_not_find_users_when_they_are_already_beneficiary(self):
        # Given
        user = users_factories.BeneficiaryGrant18Factory()
        build_user_with_ko_retryable_ubble_fraud_check(user=user)

        # When
        users = find_users_that_failed_ubble_check_seven_days_ago()

        # Then
        assert users == []

    def should_not_find_users_when_they_have_another_id_check_ok(self):
        # Given
        user = users_factories.UserFactory(dateOfBirth=self.eighteen_years_ago)
        build_user_with_ko_retryable_ubble_fraud_check(user=user)
        fraud_factories.BeneficiaryFraudCheckFactory(
            user=user,
            type=fraud_models.FraudCheckType.DMS,
            status=fraud_models.FraudCheckStatus.OK,
        )

        # When
        users = find_users_that_failed_ubble_check_seven_days_ago()

        # Then
        assert users == []

    def should_find_users_when_they_had_ok_fraud_checks_of_another_eligibility(self):
        # Given
        user = build_user_with_ko_retryable_ubble_fraud_check()
        fraud_factories.BeneficiaryFraudCheckFactory(
            user=user,
            type=fraud_models.FraudCheckType.EDUCONNECT,
            status=fraud_models.FraudCheckStatus.OK,
            eligibilityType=users_models.EligibilityType.UNDERAGE,
        )

        # When
        users = find_users_that_failed_ubble_check_seven_days_ago()

        # Then
        assert users == [user]

    def should_not_find_user_if_they_already_retried_thrice(self):
        # Given
        user = build_user_with_ko_retryable_ubble_fraud_check()
        fraud_factories.BeneficiaryFraudCheckFactory(
            user=user,
            type=fraud_models.FraudCheckType.UBBLE,
            status=fraud_models.FraudCheckStatus.KO,
        )
        fraud_factories.BeneficiaryFraudCheckFactory(
            user=user,
            type=fraud_models.FraudCheckType.UBBLE,
            status=fraud_models.FraudCheckStatus.KO,
        )

        # When
        users = find_users_that_failed_ubble_check_seven_days_ago()

        # Then
        assert users == []

    def should_not_find_user_if_they_have_a_pending_id_check(self):
        # Given
        user = build_user_with_ko_retryable_ubble_fraud_check()
        fraud_factories.BeneficiaryFraudCheckFactory(
            user=user,
            type=fraud_models.FraudCheckType.DMS,
            status=fraud_models.FraudCheckStatus.PENDING,
        )

        # When
        users = find_users_that_failed_ubble_check_seven_days_ago()

        # Then
        assert users == []
