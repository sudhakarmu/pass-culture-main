import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import React from 'react'
import { Provider } from 'react-redux'
import { MemoryRouter } from 'react-router'
import type { Store } from 'redux'

import { OfferStatus } from 'apiClient/v1'
import { Offer } from 'core/Offers/types'
import { Audience } from 'core/shared'
import { RootState } from 'store/reducers'
import { configureTestStore } from 'store/testUtils'

import OfferNameCell, { OfferNameCellProps } from '../OfferNameCell'

const renderOfferNameCell = (props: OfferNameCellProps, store: Store) => {
  render(
    <Provider store={store}>
      <MemoryRouter initialEntries={['/offres']}>
        <OfferNameCell {...props} />
      </MemoryRouter>
    </Provider>
  )
}

jest.mock('hooks/useActiveFeature', () => ({
  __esModule: true,
  default: jest.fn().mockReturnValue(true),
}))

describe('OfferNameCell', () => {
  const store: Store<RootState> = configureTestStore({})
  let defaultOffer: Offer
  beforeEach(() => {
    defaultOffer = {
      id: 'M4',
      isActive: true,
      isEditable: true,
      isEvent: true,
      hasBookingLimitDatetimesPassed: false,
      name: 'My little offer',
      thumbUrl: '/my-fake-thumb',
      status: OfferStatus.PENDING,
      educationalBooking: {
        booking_status: OfferStatus.PENDING,
        id: '1',
      },
      stocks: [],
      venue: {
        isVirtual: false,
        name: 'Paris',
        departementCode: '973',
        offererName: 'Offerer name',
      },
      isEducational: true,
    }
  })

  it('should display warning icon in name cell', () => {
    const eventOffer = {
      ...defaultOffer,
      stocks: [
        {
          beginningDatetime: new Date('2022-12-22T00:00:00Z'),
          remainingQuantity: 1,
          bookingLimitDatetime: new Date('2022-12-24T00:00:00Z'),
        },
      ],
    }

    renderOfferNameCell(
      {
        offer: eventOffer,
        editionOfferLink: '#',
        audience: Audience.COLLECTIVE,
      },
      store
    )

    const warningIco = screen.queryByAltText('Attention')
    expect(warningIco).not.toBeNull()
  })
  it('should not display warning icon in name cell', () => {
    const store: Store<RootState> = configureTestStore({})

    const eventOffer = {
      ...defaultOffer,
      stocks: [
        {
          beginningDatetime: new Date('2022-12-22T00:00:00Z'),
          remainingQuantity: 1,
          bookingLimitDatetime: new Date('2023-12-24T00:00:00Z'),
        },
      ],
    }
    renderOfferNameCell(
      {
        offer: eventOffer,
        editionOfferLink: '#',
        audience: Audience.COLLECTIVE,
      },
      store
    )

    const warningIco = screen.queryByAltText('Attention')
    expect(warningIco).toBeNull()
  })
})