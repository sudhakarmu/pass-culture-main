import { ApiError } from 'api/helpers'

import { API_ENTREPRISE_BASE_URL } from './constants'
import type {
  IEntrepriseApiJson,
  IEntrepriseSiretData,
  IEntrepriseSirenData,
} from './types'

const handleApiError = async (
  response: Response
): Promise<IEntrepriseApiJson> => {
  if (!response.ok) {
    throw new ApiError(
      response.status,
      await response.json(),
      `Échec de la requête ${response.url}, code: ${response.status}`
    )
  }

  return (await response.json()) as IEntrepriseApiJson
}

export default {
  getSiretData: async (siret: string): Promise<IEntrepriseSiretData> => {
    const response = await handleApiError(
      await fetch(`${API_ENTREPRISE_BASE_URL}/etablissements/${siret}`)
    )
    const data = response.etablissement

    return {
      address: data.geo_l4,
      city: data.libelle_commune,
      latitude: data.latitude !== null ? parseFloat(data.latitude) : null,
      longitude: data.longitude !== null ? parseFloat(data.longitude) : null,
      name:
        data.enseigne_1 ||
        data.unite_legale.denomination ||
        `${data.unite_legale.prenom_1} ${data.unite_legale.nom}` ||
        '',
      postalCode: data.code_postal,
      siret: data.siret,
      companyStatus: data.etat_administratif,
      legalUnitStatus: data.unite_legale.etat_administratif,
    }
  },

  getSirenData: async (siren: string): Promise<IEntrepriseSirenData> => {
    const response = await handleApiError(
      await fetch(`${API_ENTREPRISE_BASE_URL}/unites_legales/${siren}`)
    )

    const legalUnit = response.unite_legale

    let name
    if (legalUnit.denomination) {
      name = legalUnit.denomination
    } else if (legalUnit.etablissement_siege.enseigne_1) {
      name = legalUnit.etablissement_siege.enseigne_1
    } else {
      name = `${legalUnit.prenom_1 || ''} ${legalUnit.nom || ''}`
    }

    const latitude = legalUnit.etablissement_siege.latitude
    const longitude = legalUnit.etablissement_siege.longitude

    return {
      address: legalUnit.etablissement_siege.geo_l4,
      city: legalUnit.etablissement_siege.libelle_commune,
      latitude: latitude ? parseFloat(latitude) : null,
      longitude: longitude ? parseFloat(longitude) : null,
      name,
      postalCode: legalUnit.etablissement_siege.code_postal,
      siren: legalUnit.siren,
    }
  },
}
