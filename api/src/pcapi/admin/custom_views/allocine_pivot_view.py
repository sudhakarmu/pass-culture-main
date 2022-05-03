from pcapi.admin.base_configuration import BaseAdminView


class AllocinePivotView(BaseAdminView):
    can_create = True
    can_edit = True
    column_list = ["venue.name", "siret", "theaterId", "internalId"]
    column_searchable_list = ["venue.name", "siret", "theaterId", "internalId"]
    column_sortable_list: list[str] = []
    column_labels = {
        "theaterId": "Identifiant Allociné",
        "siret": "SIRET",
        "venue.id": "Lieu",
        "venueId": "Identifiant lieu",
        "internalId": "Identifiant interne allociné",
    }
    column_filters: list[str] = []
    form_columns = ["venueId", "siret", "theaterId", "internalId"]
