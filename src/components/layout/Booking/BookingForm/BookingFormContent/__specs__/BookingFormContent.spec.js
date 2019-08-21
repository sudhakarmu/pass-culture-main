import { shallow } from 'enzyme'
import React from 'react'
import { Field } from 'react-final-form'

import BookingFormContent from '../BookingFormContent'
import { SelectField } from '../../../../../forms/inputs'

describe('src | components | layout | Booking | BookingForm | BookingFormContent', () => {
  let props
  let handleSubmit

  beforeEach(() => {
    handleSubmit = jest.fn()
    props = {
      className: 'fake className',
      formId: 'fake formId',
      invalid: false,
      isEvent: false,
      isReadOnly: false,
      handleSubmit,
      onSetCanSubmitForm: jest.fn(),
      values: {
        bookables: [],
        date: '2019-01-01',
        price: 12,
      },
    }
  })

  it('should match snapshot', () => {
    // when
    const wrapper = shallow(<BookingFormContent {...props} />)

    // then
    expect(wrapper).toMatchSnapshot()
  })

  describe('render', () => {
    it('should render a form element with the proper props when is not read only mode', () => {
      // when
      const wrapper = shallow(<BookingFormContent {...props} />)

      // then
      const form = wrapper.find('form')
      expect(form).toHaveLength(1)
      expect(form.prop('className')).toBe('fake className')
      expect(form.prop('id')).toBe('fake formId')
      expect(form.prop('onSubmit')).toStrictEqual(handleSubmit)
    })

    it('should render a form element with the proper props when is read only mode', () => {
      // given
      props.isReadOnly = true

      // when
      const wrapper = shallow(<BookingFormContent {...props} />)

      // then
      const form = wrapper.find('form')
      expect(form).toHaveLength(1)
      expect(form.prop('className')).toBe('fake className is-read-only')
      expect(form.prop('id')).toBe('fake formId')
      expect(form.prop('onSubmit')).toStrictEqual(handleSubmit)
    })

    describe('when isEvent', () => {
      beforeEach(() => {
        props.isEvent = true
      })

      it('should render a Field component with the proper props', () => {
        // when
        const wrapper = shallow(<BookingFormContent {...props} />)

        // then
        const field = wrapper.find(Field)
        expect(field).toHaveLength(1)
        expect(field.prop('name')).toBe('date')
        expect(field.prop('render')).toStrictEqual(expect.any(Function))
      })

      it('should render a SelectField component with the right props when no date has been selected', () => {
        // when
        const wrapper = shallow(<BookingFormContent {...props} />)

        // then
        const selectField = wrapper.find(SelectField)
        expect(selectField).toHaveLength(1)
        expect(selectField.props()).toStrictEqual({
          className: 'text-center',
          disabled: false,
          id: 'booking-form-time-picker-field',
          label: 'Choisissez une heure',
          name: 'time',
          placeholder: 'Heure et prix',
          options: [],
          readOnly: false,
          required: false,
        })
      })
    })

    describe('when not isEvent', () => {
      it('should render two blocks with the proper information', () => {
        // given
        props.isEvent = false

        // when
        const wrapper = shallow(<BookingFormContent {...props} />)

        // then
        const spans = wrapper.find('span')
        expect(spans).toHaveLength(2)
        expect(spans.at(0).prop('className')).toBe('is-block')
        expect(spans.at(0).text()).toBe('Vous êtes sur le point de réserver')
        expect(spans.at(1).prop('className')).toBe('is-block')
        expect(spans.at(1).text()).toBe('cette offre pour 12 €.')
      })
    })
  })
})
