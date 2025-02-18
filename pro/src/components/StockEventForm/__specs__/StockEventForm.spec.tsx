import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Form, Formik } from 'formik'
import React from 'react'

import { renderWithProviders } from 'utils/renderWithProviders'

import { STOCK_EVENT_FORM_DEFAULT_VALUES } from '../constants'
import { stockEventFactory } from '../stockEventFactory'
import StockEventForm, { IStockEventFormProps } from '../StockEventForm'

jest.mock('utils/date', () => ({
  ...jest.requireActual('utils/date'),
  getToday: jest
    .fn()
    .mockImplementation(() => new Date('2022-12-20T00:00:00Z')),
}))

const renderStockEventForm = (
  props: IStockEventFormProps,
  initialStock = STOCK_EVENT_FORM_DEFAULT_VALUES,
  // TODO remove when WIP_ENABLE_MULTI_PRICE_STOCKS is removed
  isPriceCategoriesActive = false
) =>
  renderWithProviders(
    <Formik initialValues={{ stocks: [initialStock] }} onSubmit={() => {}}>
      <Form>
        <StockEventForm {...props} />
      </Form>
    </Formik>,
    {
      storeOverrides: {
        features: {
          list: [
            {
              isActive: isPriceCategoriesActive,
              nameKey: 'WIP_ENABLE_MULTI_PRICE_STOCKS',
            },
          ],
        },
      },
    }
  )

describe('StockEventForm', () => {
  let props: IStockEventFormProps

  beforeEach(() => {
    props = {
      today: new Date(),
      stockIndex: 0,
      priceCategoriesOptions: [
        { label: 'Tarif 1', value: '1' },
        { label: 'Tarif 2', value: '2' },
      ],
    }
  })

  // TODO delete when WIP_ENABLE_MULTI_PRICE_STOCKS is removed
  it('render StockEventForm (old)', () => {
    renderStockEventForm(props)

    expect(screen.getByLabelText('Date', { exact: true })).toBeInTheDocument()
    expect(screen.getByLabelText('Horaire')).toBeInTheDocument()
    expect(screen.getByLabelText('Tarif')).toBeInTheDocument()
    expect(
      screen.getByLabelText('Date limite de réservation')
    ).toBeInTheDocument()
    expect(screen.getByLabelText('Quantité restante')).toBeInTheDocument()

    expect(screen.getByLabelText('Date', { exact: true })).not.toBeDisabled()
    expect(screen.getByLabelText('Horaire')).not.toBeDisabled()
    expect(screen.getByLabelText('Tarif')).not.toBeDisabled()
    expect(
      screen.getByLabelText('Date limite de réservation')
    ).not.toBeDisabled()
    expect(screen.getByLabelText('Quantité restante')).not.toBeDisabled()
  })

  it('render StockEventForm', () => {
    renderStockEventForm(props, undefined, true)

    expect(screen.getByLabelText('Date', { exact: true })).toBeInTheDocument()
    expect(screen.getByLabelText('Horaire')).toBeInTheDocument()
    expect(screen.getByLabelText('Tarif')).toBeInTheDocument()
    expect(
      screen.getByLabelText('Date limite de réservation')
    ).toBeInTheDocument()
    expect(screen.getByLabelText('Quantité restante')).toBeInTheDocument()

    expect(screen.getByLabelText('Date', { exact: true })).not.toBeDisabled()
    expect(screen.getByLabelText('Horaire')).not.toBeDisabled()
    expect(screen.getByLabelText('Tarif')).not.toBeDisabled()
    expect(
      screen.getByLabelText('Date limite de réservation')
    ).not.toBeDisabled()
    expect(screen.getByLabelText('Quantité restante')).not.toBeDisabled()
  })

  it('should render disabled fields for empty form with synchronized offer in edition mode', () => {
    props.disableAllStockFields = true
    renderStockEventForm(props, { ...STOCK_EVENT_FORM_DEFAULT_VALUES })
    expect(screen.getByLabelText('Date', { exact: true })).toBeDisabled()
    expect(screen.getByLabelText('Horaire')).toBeDisabled()
    expect(screen.getByLabelText('Tarif')).toBeDisabled()
    expect(screen.getByLabelText('Date limite de réservation')).toBeDisabled()
    expect(screen.getByLabelText('Quantité restante')).toBeDisabled()
  })

  it('should not render disabled fields for empty form in edition mode for not synchronized offer', () => {
    renderStockEventForm(props, { ...STOCK_EVENT_FORM_DEFAULT_VALUES })
    expect(screen.getByLabelText('Date', { exact: true })).not.toBeDisabled()
    expect(screen.getByLabelText('Horaire')).not.toBeDisabled()
    expect(screen.getByLabelText('Tarif')).not.toBeDisabled()
    expect(
      screen.getByLabelText('Date limite de réservation')
    ).not.toBeDisabled()
    expect(screen.getByLabelText('Quantité restante')).not.toBeDisabled()
  })

  it('render disabled field in list', () => {
    renderStockEventForm(props, {
      ...STOCK_EVENT_FORM_DEFAULT_VALUES,
      readOnlyFields: [
        'beginningDate',
        'beginningTime',
        'bookingLimitDatetime',
        'price',
        'remainingQuantity',
      ],
    })

    expect(screen.getByLabelText('Date', { exact: true })).toBeDisabled()
    expect(screen.getByLabelText('Horaire')).toBeDisabled()
    expect(screen.getByLabelText('Tarif')).toBeDisabled()
    expect(screen.getByLabelText('Date limite de réservation')).toBeDisabled()
    expect(screen.getByLabelText('Quantité restante')).toBeDisabled()
  })

  it('should set stockBookingLimitDatetime at event date if date changed before stockBookingLimitDatetime', async () => {
    const initialStock = stockEventFactory({
      beginningDate: new Date('2022-12-29T00:00:00Z'),
      beginningTime: new Date('2022-12-29T00:00:00Z'),
      remainingQuantity: 11,
      bookingsQuantity: 1,
      bookingLimitDatetime: new Date('2022-12-28T00:00:00Z'),
      price: 10,
    })

    renderStockEventForm(props, initialStock)

    await userEvent.click(screen.getByLabelText('Date'))
    await userEvent.click(screen.getByText(27))

    expect(screen.getByLabelText('Date limite de réservation')).toHaveValue(
      '28/12/2022'
    )
  })

  const setNumberValueForPrice = [
    { value: '20', expectedNumber: 20 },
    { value: '20.37', expectedNumber: 20.37 },
    { value: 'azer', expectedNumber: null },
    { value: 'AZER', expectedNumber: null },
    { value: '2fsqjk', expectedNumber: 2 },
    { value: '2fsqm0', expectedNumber: 20 },
  ]
  it.each(setNumberValueForPrice)(
    'should only type numbers for price, quantity',
    async ({ value, expectedNumber }) => {
      renderStockEventForm(props)

      const priceInput = screen.getByLabelText('Tarif', {
        exact: false,
      })
      await userEvent.type(priceInput, value)
      expect(priceInput).toHaveValue(expectedNumber)
    }
  )

  const setNumberValueForQuantity = [
    { value: '20', expectedNumber: 20 },
    { value: '20.37', expectedNumber: 2037 },
    { value: '2fsqm0', expectedNumber: 20 },
  ]
  it.each(setNumberValueForQuantity)(
    'should only type numbers for price, quantity',
    async ({ value, expectedNumber }) => {
      renderStockEventForm(props)

      const quantityInput = screen.getByLabelText('Quantité restante', {
        exact: false,
      })
      await userEvent.type(quantityInput, value)
      expect(quantityInput).toHaveValue(expectedNumber)
    }
  )
})
