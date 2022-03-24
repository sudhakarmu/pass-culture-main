export interface IEntrepriseSiretData {
  address: string
  city: string
  latitude: number | null
  longitude: number | null
  name: string
  postalCode: string
  siret: string
  companyStatus: string
  legalUnitStatus: string
}

export interface IEntrepriseSirenData {
  address: string
  city: string
  latitude: number | null
  longitude: number | null
  name: string
  postalCode: string
  siren: string
}

export interface IEntrepriseApiJson {
  unite_legale: {
    prenom_1: string | null
    nom: string | null
    denomination: string | null
    etablissement_siege: {
      enseigne_1: string | null
      geo_l4: string
      libelle_commune: string
      latitude: string | null
      longitude: string | null
      code_postal: string
    }
    siren: string
  }
  etablissement: {
    enseigne_1: string | null
    geo_l4: string
    libelle_commune: string
    latitude: string | null
    longitude: string | null
    code_postal: string
    siret: string
    unite_legale: {
      prenom_1: string | null
      nom: string | null
      denomination: string | null
      etat_administratif: string
      siren: string
    }
    etat_administratif: string
  }
}
