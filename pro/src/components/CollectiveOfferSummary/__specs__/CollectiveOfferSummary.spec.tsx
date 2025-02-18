import '@testing-library/jest-dom'
import { screen, waitForElementToBeRemoved } from '@testing-library/react'
import React from 'react'

import {
  categoriesFactory,
  subCategoriesFactory,
} from 'screens/OfferEducational/__tests-utils__'
import { collectiveOfferFactory } from 'utils/collectiveApiFactories'
import { renderWithProviders } from 'utils/renderWithProviders'

import CollectiveOfferSummary, {
  ICollectiveOfferSummaryProps,
} from '../CollectiveOfferSummary'

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useParams: jest.fn(),
}))

jest.mock('apiClient/api', () => ({
  api: {
    getCollectiveOffer: jest.fn(),
    getCollectiveOfferTemplate: jest.fn(),
    getVenue: jest.fn(),
  },
}))

const renderCollectiveOfferSummary = (props: ICollectiveOfferSummaryProps) => {
  renderWithProviders(<CollectiveOfferSummary {...props} />)
}

describe('CollectiveOfferSummary', () => {
  let props: ICollectiveOfferSummaryProps
  beforeEach(() => {
    const offer = collectiveOfferFactory()
    props = {
      offer,
      categories: {
        educationalCategories: categoriesFactory([{ id: 'CAT_1' }]),
        educationalSubCategories: subCategoriesFactory([
          { categoryId: 'CAT_1', id: 'SUBCAT_1' },
        ]),
      },
    }
  })
  it('should show banner if generate from publicApi', async () => {
    const offer = collectiveOfferFactory({ isPublicApi: true })

    renderCollectiveOfferSummary({
      ...props,
      offer,
    })
    await waitForElementToBeRemoved(() => screen.queryAllByTestId('spinner'))
    expect(
      screen.getByText(
        'Offre créée par votre outil de billetterie via l’API offres collectives'
      )
    ).toBeInTheDocument()
  })
})
