import { Feature } from 'pages/AdageIframe/app/types'
import { EducationalDomain } from 'pages/AdageIframe/app/types/offers'

import { client } from './pcapiClient'

export const preBookStock = async (stockId: number): Promise<number> => {
  return client.post('/adage-iframe/bookings', { stockId })
}

export const getFeatures = async (): Promise<Feature[]> =>
  client.get('/adage-iframe/features')

export const getEducationalDomains = async (): Promise<EducationalDomain[]> =>
  client.get('/collective/educational-domains')
