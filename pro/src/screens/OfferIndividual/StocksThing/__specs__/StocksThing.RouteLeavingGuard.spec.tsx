import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import React from 'react'
import { generatePath, Route } from 'react-router'

import { api } from 'apiClient/api'
import {
  GetIndividualOfferResponseModel,
  StockResponseModel,
} from 'apiClient/v1'
import { OFFER_WIZARD_STEP_IDS } from 'components/OfferIndividualBreadcrumb'
import {
  IOfferIndividualContext,
  OfferIndividualContext,
} from 'context/OfferIndividualContext'
import { Events } from 'core/FirebaseEvents/constants'
import { OFFER_WIZARD_MODE } from 'core/Offers'
import { IOfferIndividual, IOfferIndividualVenue } from 'core/Offers/types'
import { getOfferIndividualPath } from 'core/Offers/utils/getOfferIndividualUrl'
import * as useAnalytics from 'hooks/useAnalytics'
import { ButtonLink } from 'ui-kit'
import { renderWithProviders } from 'utils/renderWithProviders'

import StocksThing, { IStocksThingProps } from '../StocksThing'

const mockLogEvent = jest.fn()

jest.mock('screens/OfferIndividual/Informations/utils', () => {
  return {
    filterCategories: jest.fn(),
  }
})

jest.mock('repository/pcapi/pcapi', () => ({
  postThumbnail: jest.fn(),
}))

jest.mock('utils/date', () => ({
  ...jest.requireActual('utils/date'),
  getToday: jest
    .fn()
    .mockImplementation(() => new Date('2020-12-15T12:00:00Z')),
}))

const renderStockThingScreen = (
  props: IStocksThingProps,
  contextValue: IOfferIndividualContext,
  url: string = generatePath(
    getOfferIndividualPath({
      step: OFFER_WIZARD_STEP_IDS.STOCKS,
      mode: OFFER_WIZARD_MODE.CREATION,
    }),
    { offerId: 'AA' }
  )
) =>
  renderWithProviders(
    <>
      <Route
        path={Object.values(OFFER_WIZARD_MODE).map(mode =>
          getOfferIndividualPath({
            step: OFFER_WIZARD_STEP_IDS.STOCKS,
            mode,
          })
        )}
      >
        <OfferIndividualContext.Provider value={contextValue}>
          <StocksThing {...props} />
          <ButtonLink link={{ to: '/outside', isExternal: false }}>
            Go outside !
          </ButtonLink>
        </OfferIndividualContext.Provider>
      </Route>
      <Route
        path={getOfferIndividualPath({
          step: OFFER_WIZARD_STEP_IDS.SUMMARY,
          mode: OFFER_WIZARD_MODE.CREATION,
        })}
      >
        <div>Next page</div>
      </Route>
      <Route
        path={getOfferIndividualPath({
          step: OFFER_WIZARD_STEP_IDS.SUMMARY,
          mode: OFFER_WIZARD_MODE.DRAFT,
        })}
      >
        <div>Next page draft</div>
      </Route>
      <Route
        path={getOfferIndividualPath({
          step: OFFER_WIZARD_STEP_IDS.STOCKS,
          mode: OFFER_WIZARD_MODE.CREATION,
        })}
      >
        <div>Save draft page</div>
      </Route>
      <Route
        path={getOfferIndividualPath({
          step: OFFER_WIZARD_STEP_IDS.INFORMATIONS,
          mode: OFFER_WIZARD_MODE.CREATION,
        })}
      >
        <div>Previous page</div>
      </Route>
      <Route path="/outside">
        <div>This is outside stock form</div>
      </Route>
    </>,
    { initialRouterEntries: [url] }
  )

describe('screens:StocksThing', () => {
  let props: IStocksThingProps
  let contextValue: IOfferIndividualContext
  let offer: Partial<IOfferIndividual>

  beforeEach(() => {
    offer = {
      id: 'OFFER_ID',
      venue: {
        departmentCode: '75',
      } as IOfferIndividualVenue,
      stocks: [],
    }
    props = {
      offer: offer as IOfferIndividual,
    }
    contextValue = {
      offerId: null,
      offer: null,
      venueList: [],
      offererNames: [],
      categories: [],
      subCategories: [],
      setOffer: () => {},
      setShouldTrack: () => {},
      shouldTrack: false,
      showVenuePopin: {},
    }
    jest
      .spyOn(api, 'getOffer')
      .mockResolvedValue({} as GetIndividualOfferResponseModel)
    jest.spyOn(useAnalytics, 'default').mockImplementation(() => ({
      logEvent: mockLogEvent,
      setLogEvent: null,
    }))
  })

  it('should not block when submitting stock when clicking on "Sauvegarder le brouillon"', async () => {
    jest.spyOn(api, 'upsertStocks').mockResolvedValue({
      stocks: [{ id: 'CREATED_STOCK_ID' } as StockResponseModel],
    })
    renderStockThingScreen(props, contextValue)

    await userEvent.type(screen.getByLabelText('Prix'), '20')
    await userEvent.click(
      screen.getByRole('button', { name: 'Sauvegarder le brouillon' })
    )
    expect(api.upsertStocks).toHaveBeenCalledTimes(1)
    expect(screen.getByText('Save draft page')).toBeInTheDocument()
  })

  it('should not block and submit stock form when click on "Étape suivante""', async () => {
    jest.spyOn(api, 'upsertStocks').mockResolvedValue({
      stocks: [{ id: 'CREATED_STOCK_ID' } as StockResponseModel],
    })
    renderStockThingScreen(props, contextValue)

    await userEvent.type(screen.getByLabelText('Prix'), '20')
    await userEvent.click(
      screen.getByRole('button', { name: 'Étape suivante' })
    )
    expect(api.upsertStocks).toHaveBeenCalledTimes(1)
    expect(screen.getByText('Next page')).toBeInTheDocument()
  })

  it('should not block when going outside and form is not touched', async () => {
    jest.spyOn(api, 'upsertStocks').mockResolvedValue({
      stocks: [{ id: 'CREATED_STOCK_ID' } as StockResponseModel],
    })

    renderStockThingScreen(props, contextValue)

    await userEvent.click(screen.getByText('Go outside !'))

    expect(screen.getByText('This is outside stock form')).toBeInTheDocument()
  })

  it('should block when clicking on "Étape précédente"', async () => {
    jest.spyOn(api, 'upsertStocks').mockResolvedValue({
      stocks: [{ id: 'CREATED_STOCK_ID' } as StockResponseModel],
    })

    renderStockThingScreen(props, contextValue)

    await userEvent.type(screen.getByLabelText('Quantité'), '20')
    await userEvent.click(
      screen.getByRole('button', { name: 'Étape précédente' })
    )
    await userEvent.click(screen.getByText('Quitter la page'))

    expect(await screen.findByText('Previous page')).toBeInTheDocument()
    expect(api.upsertStocks).not.toHaveBeenCalled()
  })

  it('should be able to stay on stock form after click on "Annuler"', async () => {
    jest.spyOn(api, 'upsertStocks').mockResolvedValue({
      stocks: [{ id: 'CREATED_STOCK_ID' } as StockResponseModel],
    })

    renderStockThingScreen(props, contextValue)
    await userEvent.type(screen.getByLabelText('Quantité'), '20')

    await userEvent.click(screen.getByText('Go outside !'))

    await userEvent.click(screen.getByText('Rester sur la page'))

    expect(screen.getByTestId('stock-thing-form')).toBeInTheDocument()
  })

  it('should be able to quit without submitting from RouteLeavingGuard', async () => {
    jest.spyOn(api, 'upsertStocks').mockResolvedValue({
      stocks: [{ id: 'CREATED_STOCK_ID' } as StockResponseModel],
    })

    renderStockThingScreen(props, contextValue)
    await userEvent.type(screen.getByLabelText('Quantité'), '20')

    await userEvent.click(screen.getByText('Go outside !'))
    expect(
      screen.getByText(
        'Restez sur la page et cliquez sur "Sauvegarder le brouillon" pour ne rien perdre de vos modifications.'
      )
    ).toBeInTheDocument()

    await userEvent.click(screen.getByText('Quitter la page'))
    expect(api.upsertStocks).toHaveBeenCalledTimes(0)

    expect(screen.getByText('This is outside stock form')).toBeInTheDocument()
  })

  it('should track when quitting without submit from RouteLeavingGuard', async () => {
    jest.spyOn(api, 'upsertStocks').mockResolvedValue({
      stocks: [{ id: 'CREATED_STOCK_ID' } as StockResponseModel],
    })
    renderStockThingScreen(props, contextValue)

    await userEvent.type(screen.getByLabelText('Prix'), '20')
    await userEvent.click(screen.getByText('Go outside !'))

    await userEvent.click(screen.getByText('Quitter la page'))

    expect(mockLogEvent).toHaveBeenCalledTimes(1)
    expect(mockLogEvent).toHaveBeenNthCalledWith(
      1,
      Events.CLICKED_OFFER_FORM_NAVIGATION,
      {
        from: 'stocks',
        isDraft: true,
        isEdition: false,
        offerId: 'OFFER_ID',
        to: '/outside',
        used: 'RouteLeavingGuard',
      }
    )
  })

  it('should be able to submit from Action Bar without Guard after changing price in draft', async () => {
    jest.spyOn(api, 'upsertStocks').mockResolvedValue({
      stocks: [{ id: 'CREATED_STOCK_ID' } as StockResponseModel],
    })
    const stock = {
      id: 'STOCK_ID',
      quantity: 10,
      price: 17.11,
      remainingQuantity: 6,
      bookingsQuantity: 0,
      hasActivationCode: false,
      activationCodesExpirationDatetime: null,
      activationCodes: [],
      beginningDatetime: null,
      bookingLimitDatetime: null,
      isSoftDeleted: false,
      isEventExpired: false,
      offerId: 'OFFER_ID',
      isEventDeletable: false,
      dateCreated: new Date(),
    }

    offer = {
      id: 'OFFER_ID',
      venue: {
        departmentCode: '75',
      } as IOfferIndividualVenue,
      stocks: [stock],
    }

    props.offer = offer as IOfferIndividual
    contextValue.offer = offer as IOfferIndividual
    renderStockThingScreen(
      props,
      contextValue,
      generatePath(
        getOfferIndividualPath({
          step: OFFER_WIZARD_STEP_IDS.STOCKS,
          mode: OFFER_WIZARD_MODE.DRAFT,
        }),
        { offerId: 'AA' }
      )
    )
    await userEvent.type(screen.getByLabelText('Prix'), '20')

    await userEvent.click(screen.getByText('Étape suivante'))
    expect(api.upsertStocks).toHaveBeenCalledTimes(1)

    expect(screen.getByText('Next page draft')).toBeInTheDocument()
  })
})
