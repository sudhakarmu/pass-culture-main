import datetime
import typing

import pydantic

from pcapi.core.fraud import models as fraud_models
import pcapi.core.history.models as history_models
import pcapi.core.offerers.models as offerers_models
from pcapi.core.subscription import models as subscription_models
from pcapi.core.subscription.phone_validation import exceptions as phone_validation_exceptions
from pcapi.core.users import models as users_models
from pcapi.models.validation_status_mixin import ValidationStatus
from pcapi.routes.serialization import BaseModel
from pcapi.utils import phone_number as phone_number_utils
from pcapi.utils.email import sanitize_email


class Permission(BaseModel):
    class Config:
        orm_mode = True

    id: int
    name: str
    category: str | None


class Role(BaseModel):
    class Config:
        orm_mode = True

    id: int
    name: str
    permissions: list[Permission]


class ListRoleResponseModel(BaseModel):
    class Config:
        orm_mode = True

    roles: list[Role]


class ListPermissionResponseModel(BaseModel):
    class Config:
        orm_mode = True

    permissions: list[Permission]


class RoleRequestModel(BaseModel):
    name: str = pydantic.Field(..., min_length=1)
    permissionIds: list[int]


class PublicAccount(BaseModel):
    class Config:
        orm_mode = True
        use_enum_values = True

    id: int
    firstName: str | None
    lastName: str | None
    dateOfBirth: datetime.datetime | None
    email: str
    phoneNumber: str | None
    roles: list[users_models.UserRole]
    isActive: bool
    address: str | None
    postalCode: str | None
    city: str | None


class PaginableQuery(BaseModel):
    page: int | None = 1
    perPage: int | None = 20
    sort: str | None = None


class FilterableQuery(BaseModel):
    filter: str | None = None


class OffererToBeValidatedQuery(PaginableQuery, FilterableQuery):
    q: str | None


class UserOffererToBeValidatedQuery(PaginableQuery, FilterableQuery):
    pass


class SearchQuery(PaginableQuery):
    q: str

    @pydantic.validator("q")
    def validate_q(cls, q: str) -> str:
        if "%" in q:
            raise ValueError(f"Le caractère % n'est pas autorisé : {q}")
        return q


class Response(BaseModel):
    data: typing.Any


class PaginatedResponse(Response):
    pages: int
    total: int
    page: int
    size: int
    sort: str | None


class ListPublicAccountsResponseModel(PaginatedResponse):
    data: list[PublicAccount]


class PublicAccountUpdateRequest(BaseModel):
    firstName: str | None
    lastName: str | None
    dateOfBirth: datetime.datetime | None
    idPieceNumber: str | None
    email: pydantic.EmailStr | None
    phoneNumber: str | None
    address: str | None
    postalCode: str | None
    city: str | None

    @pydantic.validator("email", pre=True)
    def validate_email(cls, email: str) -> str:
        if not email:
            return email
        return sanitize_email(email)

    @pydantic.validator("phoneNumber")
    def validate_phone_number(cls, phone_number: str) -> str:
        if not phone_number:
            return phone_number

        try:
            # Convert to international format
            return phone_number_utils.ParsedPhoneNumber(phone_number).phone_number
        except phone_validation_exceptions.InvalidPhoneNumber:
            raise ValueError(f"Format de numéro de téléphone invalide : {phone_number}")


class GetBeneficiaryCreditResponseModel(BaseModel):
    initialCredit: float
    remainingCredit: float
    remainingDigitalCredit: float
    dateCreated: datetime.datetime | None


class AuthTokenQuery(BaseModel):
    token: str


class AuthTokenResponseModel(BaseModel):
    token: str


class SubscriptionItemModel(BaseModel):
    class Config:
        orm_mode = True
        use_enum_values = True

    type: subscription_models.SubscriptionStep
    status: subscription_models.SubscriptionItemStatus


class IdCheckItemModel(BaseModel):
    class Config:
        orm_mode = True
        use_enum_values = True

    @classmethod
    def from_orm(cls, fraud_check: fraud_models.BeneficiaryFraudCheck) -> "IdCheckItemModel":
        fraud_check.technicalDetails = fraud_check.resultContent

        if fraud_check.type == fraud_models.FraudCheckType.DMS and fraud_check.resultContent is not None:
            dms_content = fraud_models.DMSContent(**fraud_check.resultContent)  # type: ignore [arg-type]
            fraud_check.sourceId = str(dms_content.procedure_number)

        return super().from_orm(fraud_check)

    type: fraud_models.FraudCheckType
    dateCreated: datetime.datetime
    thirdPartyId: str
    status: fraud_models.FraudCheckStatus | None
    reason: str | None
    reasonCodes: list[fraud_models.FraudReasonCode] | None
    technicalDetails: dict | None
    sourceId: str | None = None  # DMS only


class EligibilitySubscriptionHistoryModel(BaseModel):
    subscriptionItems: list[SubscriptionItemModel]
    idCheckHistory: list[IdCheckItemModel]


class GetUserSubscriptionHistoryResponseModel(BaseModel):
    subscriptions: dict[str, EligibilitySubscriptionHistoryModel]


class BeneficiaryReviewRequestModel(BaseModel):
    class Config:
        extra = pydantic.Extra.forbid

    reason: str
    review: fraud_models.FraudReviewStatus
    eligibility: str | None


class BeneficiaryReviewResponseModel(BaseModel):
    reason: str | None
    review: fraud_models.FraudReviewStatus
    eligibility: str | None
    userId: int
    authorId: int


class PublicHistoryItem(BaseModel):
    class config:
        extra = pydantic.Extra.forbid

    action: str
    datetime: datetime.datetime
    message: str


class PublicHistoryResponseModel(BaseModel):
    history: list[PublicHistoryItem]


class ProSearchQuery(PaginableQuery):
    q: str
    type: str  # "proUser" or "venue" or "offerer"

    @pydantic.validator("q")
    def validate_q(cls, q: str) -> str:
        if "%" in q:
            raise ValueError(f"Le caractère % n'est pas autorisé : {q}")
        return q


class ProResultPayload(BaseModel):
    class Config:
        orm_mode = True
        use_enum_values = True


class ProUserPayload(ProResultPayload):
    firstName: str | None
    lastName: str | None
    email: str
    phoneNumber: str | None
    isActive: bool


class OffererPayload(ProResultPayload):
    name: str | None
    siren: str | None
    validationStatus: ValidationStatus
    isActive: bool


class VenuePayload(ProResultPayload):
    name: str | None
    email: str | None
    siret: str | None
    permanent: bool
    validationStatus: ValidationStatus
    isActive: bool

    @classmethod
    def from_orm(cls: typing.Type["VenuePayload"], venue: offerers_models.Venue) -> "VenuePayload":
        if venue.contact and venue.contact.email:
            venue.email = venue.contact.email
        else:
            venue.email = venue.bookingEmail
        venue.permanent = venue.isPermanent
        venue.validationStatus = venue.managingOfferer.validationStatus
        venue.isActive = venue.managingOfferer.isActive
        return super().from_orm(venue)


class ProResult(BaseModel):
    resourceType: str  # "proUser" or "venue" or "offerer"
    id: int
    payload: ProResultPayload


class SearchProResponseModel(PaginatedResponse):
    data: list[ProResult]


class OffererAttachedUser(BaseModel):
    class Config:
        orm_mode = True
        use_enum_values = True

    id: int  # user id
    firstName: str | None
    lastName: str | None
    email: str
    phoneNumber: str | None
    user_offerer_id: int
    validationStatus: ValidationStatus


class OffererAttachedUsersResponseModel(BaseModel):
    data: list[OffererAttachedUser]


class OffererBankInformationStatus(BaseModel):
    """
    le nombre de lieux dont les infos permettent (ok), ou pas (ko), les remboursements
    """

    ko: int
    ok: int


class BaseOffersStats(BaseModel):
    individual: int
    collective: int


class OffersStats(BaseModel):
    active: BaseOffersStats
    inactive: BaseOffersStats


class ReimbursementsStats(BaseModel):
    done: int
    pending: int
    upcoming: int


class OffererBasicInfo(BaseModel):
    class Config:
        use_enum_values = True

    id: int
    name: str
    validationStatus: ValidationStatus
    isActive: bool
    siren: str | None
    region: str
    bankInformationStatus: OffererBankInformationStatus
    isCollectiveEligible: bool


class VenueDmsStats(BaseModel):
    status: str
    subscriptionDate: datetime.datetime
    url: str


class VenueBasicInfo(BaseModel):
    id: int
    name: str
    siret: str | None
    email: str | None
    phoneNumber: str | None
    region: str
    hasReimbursementPoint: bool
    isCollectiveEligible: bool
    dms: VenueDmsStats | None


class LastOfferSyncStats(BaseModel):
    date: datetime.datetime | None
    provider: str | None


class VenueOffersStats(OffersStats):
    lastSync: LastOfferSyncStats


class OffererTagItem(BaseModel):
    class Config:
        orm_mode = True

    id: int
    name: str
    label: str | None


class OffererTagsResponseModel(BaseModel):
    data: list[OffererTagItem]


class OffererBasicInfoResponseModel(Response):
    data: OffererBasicInfo


class OffererTotalRevenueResponseModel(Response):
    data: float


class OffererOfferStatsResponseModel(Response):
    data: OffersStats


class HistoryItem(BaseModel):
    class Config:
        use_enum_values = True

    type: history_models.ActionType
    date: str | None
    authorId: int | None  # backoffice user OR pro user who made the action
    authorName: str | None
    comment: str | None
    accountId: int | None  # pro user attached to the offerer
    accountName: str | None


class HistoryResponseModel(Response):
    data: list[HistoryItem]


class Comment(BaseModel):
    date: str | None
    author: str | None
    content: str


class OfferersStatsResponseModel(BaseModel):
    data: dict[str, int]  # keys are validationStatus names


class OffererToBeValidated(BaseModel):
    id: int
    name: str
    dateCreated: str
    status: str
    step: str | None
    siren: str | None
    address: str | None  # nullable in HasAddressMixin
    postalCode: str
    city: str
    owner: str | None
    ownerId: int | None
    phoneNumber: str | None
    email: str | None
    lastComment: Comment | None
    isTopActor: bool


class ListOffererToBeValidatedResponseModel(PaginatedResponse):
    data: list[OffererToBeValidated]


class OptionalCommentRequest(BaseModel):
    comment: str | None


class CommentRequest(BaseModel):
    comment: str


class IsTopActorRequest(BaseModel):
    isTopActor: bool


class UserOffererToBeValidated(BaseModel):
    id: int
    userId: int
    email: str | None
    userName: str
    status: str
    dateCreated: str | None
    lastComment: Comment | None
    phoneNumber: str | None
    offererId: int
    offererName: str
    offererCreatedDate: str
    ownerId: int | None
    ownerEmail: str | None
    siren: str


class ListUserOffererToBeValidatedResponseModel(PaginatedResponse):
    data: list[UserOffererToBeValidated]
