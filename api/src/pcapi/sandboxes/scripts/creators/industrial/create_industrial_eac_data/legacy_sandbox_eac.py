from dataclasses import dataclass
import datetime
from itertools import chain
from itertools import cycle
from typing import Any

from pcapi.core.educational import models as educational_models
import pcapi.core.educational.factories as educational_factories
from pcapi.core.offerers import models as offerers_models
import pcapi.core.offerers.factories as offerers_factories
from pcapi.models import offer_mixin
from pcapi.utils.human_ids import humanize
from pcapi.utils.image_conversion import DO_NOT_CROP


@dataclass
class StockData:
    name: str
    price: int
    timedelta: int
    numberOfTickets: int
    addressType: str
    otherAddress: str
    interventionArea: list[str]
    educationalInstitutionId: str | None
    imageName: str | None = None
    lastValidationDate: datetime.datetime | None = None
    lastValidationType: offer_mixin.OfferValidationType | None = None
    validation: offer_mixin.OfferValidationStatus | None = None
    isActive: bool | None = None


@dataclass
class TemplateOfferData:
    name: str
    addressType: str
    otherAddress: str
    interventionArea: list[str]
    imageName: str | None = None


FAKE_STOCK_DATA = [
    StockData(
        name="Visite de l'Abbaye Royale + Musée d'art moderne + Nocturne Les étoiles de Fontevraud",
        price=1000,
        timedelta=20,
        numberOfTickets=10,
        addressType="other",
        otherAddress="1 rue des polissons, Paris 75017",
        interventionArea=[],
        educationalInstitutionId=None,
        imageName="collective_offer.png",
    ),
    StockData(
        name="Visite de la mine Gabe Gottes",
        price=800,
        timedelta=18,
        numberOfTickets=30,
        addressType="school",
        otherAddress="",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
    StockData(
        name="Clued'au Château",
        price=1200,
        timedelta=15,
        numberOfTickets=25,
        addressType="other",
        otherAddress="1 rue des polissons, Paris 75017",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
    StockData(
        name="Visitez le Panthéon, Chef d'œuvre de l'architecte Soufflot",
        price=1200,
        timedelta=22,
        numberOfTickets=20,
        addressType="offererVenue",
        otherAddress="",
        interventionArea=[],
        educationalInstitutionId="0780032L-2",
    ),
    StockData(
        name="Arc de Triomphe : embrassez tout Paris du haut du monument emblématique",
        price=1200,
        timedelta=25,
        numberOfTickets=5,
        addressType="other",
        otherAddress="1 rue des polissons, Paris 75017",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
    StockData(
        name="Site archéologique : un des plus vieux villages d'Europe (2500 ans avant JC)",
        price=1200,
        timedelta=27,
        numberOfTickets=40,
        addressType="school",
        otherAddress="",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
    StockData(
        name="Spectacle nocturne Lux Salina",
        price=600,
        timedelta=8,
        numberOfTickets=50,
        addressType="other",
        otherAddress="1 rue des polissons, Paris 75017",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
    StockData(
        name="Découverte des métiers du patrimoine: Restaurateur(trice) Décorateur(trice), Doreur(reuse)",
        price=900,
        timedelta=5,
        numberOfTickets=15,
        addressType="offererVenue",
        otherAddress="",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
    StockData(
        name="Entrée 'Spectacle aux Étoiles' avec conférence 'La Lune... connue et inconnue'",
        price=860,
        timedelta=9,
        numberOfTickets=100,
        addressType="school",
        otherAddress="",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
    StockData(
        name="Le Grognement de la voie lactée - Bonn Park/Paul Moulin, Maia Sandoz",
        price=400,
        timedelta=5,
        numberOfTickets=10,
        addressType="school",
        otherAddress="",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
    StockData(
        name="Baal - Bertolt Brecht / Armel Roussel",
        price=200,
        timedelta=2,
        numberOfTickets=80,
        addressType="offererVenue",
        otherAddress="",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
    StockData(
        name="Intervention Estampe en Partage - Collège Les Célestins de Vichy",
        price=100,
        timedelta=18,
        numberOfTickets=12,
        addressType="offererVenue",
        otherAddress="",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
    StockData(
        name="Sensibilisation au jazz par une approche vivante en lien avec 'Anglet Jazz Festival'",
        price=150,
        timedelta=10,
        numberOfTickets=50,
        addressType="offererVenue",
        otherAddress="",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
    StockData(
        name="L'art de la mosaïque sur la colline de Fourvière",
        price=150,
        timedelta=10,
        numberOfTickets=50,
        addressType="offererVenue",
        otherAddress="",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
    StockData(
        name="À la découverte de la lignée évolutive humaine",
        price=150,
        timedelta=10,
        numberOfTickets=50,
        addressType="offererVenue",
        otherAddress="",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
    StockData(
        name="offre en région parisienne",
        price=1000,
        timedelta=20,
        numberOfTickets=10,
        addressType="other",
        otherAddress="1 rue des polissons, Paris 75017",
        interventionArea=["75", "92", "93", "94", "78", "91", "95"],
        educationalInstitutionId=None,
    ),
    StockData(
        name="offre en martinique",
        price=800,
        timedelta=18,
        numberOfTickets=30,
        addressType="school",
        otherAddress="",
        interventionArea=["972"],
        educationalInstitutionId=None,
    ),
    StockData(
        name="offre en corse",
        price=1200,
        timedelta=15,
        numberOfTickets=25,
        addressType="other",
        otherAddress="1 rue des polissons, Paris 75017",
        interventionArea=["2A", "2B"],
        educationalInstitutionId=None,
    ),
    StockData(
        name="offre en Loire-Atlantique visible uniquement pas l'etablissement 1",
        price=1200,
        timedelta=22,
        numberOfTickets=20,
        addressType="offererVenue",
        otherAddress="",
        interventionArea=["44"],
        educationalInstitutionId="0780032L-2",
    ),
    StockData(
        name="offre refusée",
        price=1200,
        timedelta=22,
        numberOfTickets=20,
        addressType="offererVenue",
        otherAddress="",
        interventionArea=["44"],
        educationalInstitutionId=None,
        lastValidationDate=datetime.datetime.utcnow(),
        lastValidationType=offer_mixin.OfferValidationType.MANUAL,
        validation=offer_mixin.OfferValidationStatus.REJECTED,
    ),
    StockData(
        name="offre en attente de validation",
        price=1200,
        timedelta=22,
        numberOfTickets=20,
        addressType="offererVenue",
        otherAddress="",
        interventionArea=["44"],
        educationalInstitutionId=None,
        validation=offer_mixin.OfferValidationStatus.PENDING,
    ),
    StockData(
        name="brouillon d'offre",
        price=1200,
        timedelta=22,
        numberOfTickets=20,
        addressType="offererVenue",
        otherAddress="",
        interventionArea=["44"],
        educationalInstitutionId=None,
        validation=offer_mixin.OfferValidationStatus.DRAFT,
    ),
    StockData(
        name="offre innactive",
        price=1200,
        timedelta=22,
        numberOfTickets=20,
        addressType="offererVenue",
        otherAddress="",
        interventionArea=["44"],
        educationalInstitutionId=None,
        isActive=False,
    ),
]

PASSED_STOCK_DATA: list[StockData] = [
    StockData(
        name="Passée: Spectacle nocturne Lux Salina",
        price=600,
        timedelta=8,
        numberOfTickets=50,
        addressType="other",
        otherAddress="1 rue des polissons, Paris 75017",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
    StockData(
        name="Passée: Découverte des métiers du patrimoine: Restaurateur(trice) Décorateur(trice), Doreur(reuse)",
        price=900,
        timedelta=5,
        numberOfTickets=15,
        addressType="offererVenue",
        otherAddress="",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
    StockData(
        name="Passée: Entrée 'Spectacle aux Étoiles' avec conférence 'La Lune... connue et inconnue'",
        price=860,
        timedelta=9,
        numberOfTickets=100,
        addressType="school",
        otherAddress="",
        interventionArea=[],
        educationalInstitutionId=None,
    ),
]

MAINLAND_INTERVENTION_AREA = [str(i).zfill(2) for i in chain(range(1, 95), ["2A", "2B", "mainland"]) if i != 20]
ALL_INTERVENTION_AREA = [
    *MAINLAND_INTERVENTION_AREA,
    "971",
    "972",
    "973",
    "974",
    "975",
    "976",
    "all",
]


def add_image_to_offer(offer: educational_models.HasImageMixin, image_name: str) -> None:
    with open(
        f"./src/pcapi/sandboxes/thumbs/collectif/{image_name}",
        mode="rb",
    ) as file:
        offer.set_image(image=file.read(), credit="CC-BY-SA WIKIPEDIA", crop_params=DO_NOT_CROP)


TEMPLATE_OFFERS_DATA = [
    TemplateOfferData(
        name="Visite du studio d'enregistrement de l'EAC collectif",
        addressType="offererVenue",
        otherAddress="",
        interventionArea=[],
    ),
    TemplateOfferData(
        name="Plongez au coeur de la pâtisserie du 12 rue Duhesme",
        addressType="other",
        otherAddress="12 rue Duhesme, Paris 75018",
        interventionArea=[],
    ),
    TemplateOfferData(
        name="Une offre vitrine pas comme les autres",
        addressType="school",
        otherAddress="",
        interventionArea=[],
        imageName="collective_offer_template.jpg",
    ),
    TemplateOfferData(
        name="Une offre vitrine pour les Bouches-du-Rhône ",
        addressType="offererVenue",
        otherAddress="",
        interventionArea=["13"],
    ),
    TemplateOfferData(
        name="Une offre vitrine pour toute la france metro",
        addressType="offererVenue",
        otherAddress="",
        interventionArea=MAINLAND_INTERVENTION_AREA,
    ),
]
ADDRESSES = [
    {"department": "04", "postalCode": "04400", "city": "Barcelonnette"},
    {"department": "14", "postalCode": "14000", "city": "Caen"},
    {"department": "44", "postalCode": "44119", "city": "Treillières"},
    {"department": "52", "postalCode": "52300", "city": "Joinville"},
    {"department": "71", "postalCode": "71400", "city": "Autun"},
    {"department": "78", "postalCode": "78646", "city": "Versailles"},
    {"department": "83", "postalCode": "83230", "city": "Bormes-Les-Mimosas"},
    {"department": "85", "postalCode": "85350", "city": "L'île-d'Yeu"},
    {"department": "971", "postalCode": "97140", "city": "Marie-Galante"},
    {"department": "974", "postalCode": "97410", "city": "Saint-Benoît"},
]

VENUE_EDUCATIONAL_STATUS = {
    2: "Établissement public",
    3: "Association",
    4: "Établissement privé",
    5: "micro-entreprise, auto-entrepreneur",
}


educational_domain_cursor = 0


def create_industrial_educational_bookings() -> None:
    educational_current_year = educational_factories.EducationalYearFactory()
    educational_next_year = educational_factories.EducationalYearFactory()

    educational_factories.EducationalInstitutionFactory.create_batch(20)

    educational_institutions = [
        educational_factories.EducationalInstitutionFactory(institutionId="0780032L-2"),
        educational_factories.EducationalInstitutionFactory(institutionId="0752525M-2"),
        educational_factories.EducationalInstitutionFactory(institutionId="0760100W-2"),
        educational_factories.EducationalInstitutionFactory(institutionId="0921545E-2"),
        educational_factories.EducationalInstitutionFactory(
            institutionId="0910620E-2",
            institutionType="LYCEE POLYVALENT",
            name="LYC METIER ROBERT DOISNEAU",
            city="CORBEIL-ESSONNES",
            postalCode="91100",
        ),
        educational_factories.EducationalInstitutionFactory(
            institutionId="0221518F-2",
            email=None,
            institutionType="COLLEGE",
            name="FRANCOIS CLECH",
            city="BEGARD",
            postalCode="22140",
        ),
        educational_factories.EducationalInstitutionFactory(
            institutionId="0010819K-2",
            name="LYC LES SARDIERES - BOURG EN BRESS",
            institutionType="",
            city="BOURG-EN-BRESSE",
            postalCode="01000",
        ),
    ]
    offerer_with_right_siren = offerers_factories.CollectiveOffererFactory(
        name="Bonne structure pour l'EAC sans siren",
    )
    offerers_factories.VirtualVenueFactory(
        name="Lieu virtuel Bonne structure pour l'EAC", managingOfferer=offerer_with_right_siren
    )

    venues = []
    venues.append(
        offerers_factories.CollectiveVenueFactory(
            name="[EAC] Opéra Royal de Versailles - Salle 1",
            managingOfferer=offerer_with_right_siren,
            adageId=None,
            venueEducationalStatus=get_venueEducationalStatus_by_id((1 % len(VENUE_EDUCATIONAL_STATUS)) + 2),
            collectiveDomains=[get_educational_domain(), get_educational_domain()],
            collectiveNetwork=["127830", "128029", "130265"],
            collectiveInterventionArea=ALL_INTERVENTION_AREA,
            pricing_point="self",
            reimbursement_point="self",
            venueLabelId=7,
        )
    )
    venues.append(
        offerers_factories.CollectiveVenueFactory(
            name="[EAC] Opéra Royal de Versailles - Salle 2",
            managingOfferer=offerer_with_right_siren,
            adageId=None,
            venueEducationalStatus=get_venueEducationalStatus_by_id((2 % len(VENUE_EDUCATIONAL_STATUS)) + 2),
            collectiveDomains=[get_educational_domain()],
            collectiveNetwork=["127344"],
            collectiveInterventionArea=MAINLAND_INTERVENTION_AREA,
            pricing_point="self",
            reimbursement_point="self",
            venueLabelId=24,
        )
    )
    venues.append(
        offerers_factories.CollectiveVenueFactory(
            name="[EAC] Opéra Royal de Versailles - Salle 3",
            managingOfferer=offerer_with_right_siren,
            adageId=None,
            venueEducationalStatus=get_venueEducationalStatus_by_id((3 % len(VENUE_EDUCATIONAL_STATUS)) + 2),
            collectiveDomains=[get_educational_domain(), get_educational_domain(), get_educational_domain()],
            collectiveNetwork=["126531", "130079"],
            pricing_point="self",
            reimbursement_point="self",
            venueLabelId=22,
            venueTypeCode=offerers_models.VenueTypeCode.ADMINISTRATIVE,
        )
    )

    cnl_like_offerer = offerers_factories.CollectiveOffererFactory(name="[EAC] Structure factice CNL")
    for i in range(0, 3):
        venues.append(
            offerers_factories.CollectiveVenueFactory(
                siret=None,
                managingOfferer=cnl_like_offerer,
                name=f"[EAC] Lieu factice du CNL {i}",
                comment="Ce lieu est un lieu fictif créé pour les tests de l'EAC",
                venueEducationalStatus=get_venueEducationalStatus_by_id((i + 3))
                if (i + 3) in VENUE_EDUCATIONAL_STATUS
                else None,
                venueLabelId=None,
            )
        )

    educational_redactor = educational_factories.EducationalRedactorFactory(email="compte.test@education.gouv.fr")

    for address in ADDRESSES:
        venues.append(
            offerers_factories.CollectiveVenueFactory(
                departementCode=address["department"],
                city=address["city"],
                postalCode=address["postalCode"],
                pricing_point="self",
                reimbursement_point="self",
            )
        )

    for venue in venues:
        offerers_factories.UserOffererFactory(offerer=venue.managingOfferer)

    deposits = []
    for educational_institution in educational_institutions:
        if educational_institution.institutionId == "0010819K-2":
            deposits.append(
                educational_factories.EducationalDepositFactory(
                    ministry=educational_models.Ministry.AGRICULTURE,
                    educationalInstitution=educational_institution,
                    educationalYear=educational_current_year,
                    amount=40000,
                )
            )
            deposits.append(
                educational_factories.EducationalDepositFactory(
                    ministry=educational_models.Ministry.AGRICULTURE,
                    educationalInstitution=educational_institution,
                    educationalYear=educational_next_year,
                    amount=50000,
                    isFinal=False,
                )
            )
        else:
            deposits.append(
                educational_factories.EducationalDepositFactory(
                    educationalInstitution=educational_institution,
                    educationalYear=educational_current_year,
                    amount=40000,
                )
            )
            deposits.append(
                educational_factories.EducationalDepositFactory(
                    educationalInstitution=educational_institution,
                    educationalYear=educational_next_year,
                    amount=50000,
                    isFinal=False,
                )
            )

    now = datetime.datetime.utcnow()
    stocks: list[educational_models.CollectiveStock] = []
    passed_stocks: list[educational_models.CollectiveStock] = []
    next_year_stocks: list[educational_models.CollectiveStock] = []

    for stock_data, venue in zip(FAKE_STOCK_DATA, cycle(venues)):
        stocks.append(_create_collective_stock(stock_data, now, venue, number_of_stocks=2, is_passed=False)[0])

    for stock_data, venue in zip(PASSED_STOCK_DATA, cycle(venues)):
        passed_stocks.append(_create_collective_stock(stock_data, now, venue, number_of_stocks=2, is_passed=True)[0])

    for stock_data, venue in zip(FAKE_STOCK_DATA, cycle(venues)):
        next_year_stocks.append(
            _create_collective_stock(
                stock_data, educational_next_year.beginningDate, venue, number_of_stocks=2, is_passed=False
            )[0]
        )

    for stock_data, venue in zip(FAKE_STOCK_DATA, cycle(venues)):
        template = educational_factories.CollectiveOfferTemplateFactory(
            educational_domains=[get_educational_domain()], venue=venue
        )
        stocks.append(
            _create_collective_stock(stock_data, now, venue, number_of_stocks=2, is_passed=False, parent=template)[0]
        )

    for index, stock, educational_institution in zip(range(len(stocks)), stocks, cycle(educational_institutions)):
        if index % 4 == 0:
            educational_factories.PendingCollectiveBookingFactory(
                educationalRedactor=educational_redactor,
                educationalInstitution=educational_institution,
                educationalYear=educational_current_year,
                collectiveStock=stock,
            )
        elif index % 4 == 1:
            educational_factories.CancelledCollectiveBookingFactory(
                educationalRedactor=educational_redactor,
                educationalInstitution=educational_institution,
                educationalYear=educational_current_year,
                collectiveStock=stock,
            )
        elif index % 4 == 2:
            educational_factories.ConfirmedCollectiveBookingFactory(
                educationalRedactor=educational_redactor,
                educationalInstitution=educational_institution,
                educationalYear=educational_current_year,
                collectiveStock=stock,
            )
        else:
            educational_factories.ReimbursedCollectiveBookingFactory(
                educationalRedactor=educational_redactor,
                educationalInstitution=educational_institution,
                educationalYear=educational_current_year,
                collectiveStock=stock,
            )

    for stock, educational_institution in zip(passed_stocks, cycle(educational_institutions)):
        educational_factories.UsedCollectiveBookingFactory(
            educationalRedactor=educational_redactor,
            educationalInstitution=educational_institution,
            educationalYear=educational_current_year,
            dateUsed=now - datetime.timedelta(8),
            collectiveStock=stock,
            collectiveStock__beginningDatetime=now - datetime.timedelta(8),
        )

    for next_year_stock, educational_institution in zip(next_year_stocks, cycle(educational_institutions)):
        educational_factories.PendingCollectiveBookingFactory(
            educationalRedactor=educational_redactor,
            educationalInstitution=educational_institution,
            educationalYear=educational_next_year,
            confirmationLimitDate=now + datetime.timedelta(days=30),
            collectiveStock=next_year_stock,
        )

    for template_data in TEMPLATE_OFFERS_DATA:
        _create_collective_offer_template(template_data, venue)


def _create_collective_stock(
    stock_data: StockData,
    now: datetime.datetime,
    venue: offerers_models.Venue,
    number_of_stocks: int = 2,
    is_passed: bool = False,
    parent: educational_models.CollectiveOfferTemplate | None = None,
) -> list[educational_models.CollectiveStock]:
    timedelta = int(stock_data.timedelta)
    kwargs: dict[str, Any] = {}
    if is_passed:
        beginningDatetime = now - datetime.timedelta(days=timedelta)
    else:
        beginningDatetime = now + datetime.timedelta(days=timedelta)

    educational_institution = None
    if stock_data.educationalInstitutionId:
        educational_institution = educational_models.EducationalInstitution.query.filter(
            educational_models.EducationalInstitution.institutionId == stock_data.educationalInstitutionId
        ).one()

    if stock_data.lastValidationDate:
        kwargs["collectiveoffer__lastValidationDate"] = stock_data.lastValidationDate
    if stock_data.lastValidationType:
        kwargs["collectiveoffer__lastValidationType"] = stock_data.lastValidationType
    if stock_data.validation:
        kwargs["collectiveoffer__validation"] = stock_data.validation
    if stock_data.isActive is not None:
        kwargs["collectiveoffer__isActive"] = stock_data.isActive

    stocks = educational_factories.CollectiveStockFactory.create_batch(
        number_of_stocks,
        price=stock_data.price,
        beginningDatetime=beginningDatetime,
        numberOfTickets=stock_data.numberOfTickets,
        collectiveOffer__durationMinutes=60,
        collectiveOffer__description="Une description multi-lignes.\nUn lien en description ? https://youtu.be/dQw4w9WgXcQ\n Un email ? mon.email@example.com",
        collectiveOffer__name=stock_data.name,
        collectiveOffer__venue=venue,
        collectiveOffer__students=[
            educational_models.StudentLevels.CAP1,
            educational_models.StudentLevels.CAP2,
            educational_models.StudentLevels.GENERAL1,
            educational_models.StudentLevels.GENERAL2,
        ],
        collectiveOffer__offerVenue={
            "addressType": stock_data.addressType,
            "otherAddress": stock_data.otherAddress,
            "venueId": humanize(venue.id),
        },
        collectiveOffer__contactEmail="miss.rond@point.com",
        collectiveOffer__contactPhone="0101010101",
        collectiveOffer__motorDisabilityCompliant=True,
        collectiveOffer__visualDisabilityCompliant=True,
        collectiveOffer__interventionArea=stock_data.interventionArea,
        collectiveOffer__institution=educational_institution,
        collectiveOffer__educational_domains=[get_educational_domain()],
        collectiveOffer__template=parent,
    )
    if stock_data.imageName is not None and stocks:
        add_image_to_offer(offer=stocks[0].collectiveOffer, image_name=stock_data.imageName)
    return stocks


def _create_collective_offer_template(
    offer_data: TemplateOfferData,
    venue: offerers_models.Venue,
) -> None:
    offer = educational_factories.CollectiveOfferTemplateFactory(
        name=offer_data.name,
        durationMinutes=60,
        description="Une description multi-lignes.\nUn lien en description ? https://youtu.be/dQw4w9WgXcQ\n Un email ? mon.email@example.com",
        venue=venue,
        students=[
            educational_models.StudentLevels.CAP1,
            educational_models.StudentLevels.GENERAL1,
        ],
        offerVenue={
            "addressType": offer_data.addressType,
            "otherAddress": offer_data.otherAddress,
            "venueId": humanize(venue.id),
        },
        contactEmail="miss.rond@point.com",
        contactPhone="0101010101",
        motorDisabilityCompliant=True,
        visualDisabilityCompliant=True,
        interventionArea=offer_data.interventionArea,
        educational_domains=[get_educational_domain()],
    )
    if offer_data.imageName is not None:
        add_image_to_offer(offer=offer, image_name=offer_data.imageName)


def get_educational_domain() -> educational_models.EducationalDomain:
    global educational_domain_cursor  # pylint: disable=global-statement
    total = educational_models.EducationalDomain.query.count() - 1
    educational_domain_cursor = (educational_domain_cursor % total) + 1
    return educational_models.EducationalDomain.query.filter_by(id=educational_domain_cursor).one()


def get_venueEducationalStatus_by_id(status_id: int) -> offerers_models.VenueEducationalStatus:
    return offerers_models.VenueEducationalStatus.query.filter_by(id=status_id).one()
