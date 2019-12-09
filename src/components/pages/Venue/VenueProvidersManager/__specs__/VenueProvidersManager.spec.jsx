import { shallow } from 'enzyme'
import React from 'react'

import VenueProvidersManager from '../VenueProvidersManager'
import VenueProviderItem from '../VenueProviderItem/VenueProviderItem'
import AllocineProviderFormContainer from '../AllocineProviderForm/AllocineProviderFormContainer'

describe('src | components | pages | Venue | VenueProvidersManager', () => {
  let props
  let loadProvidersAndVenueProviders
  let history

  beforeEach(() => {
    history = {
      push: jest.fn(),
    }
    loadProvidersAndVenueProviders = jest.fn()
    props = {
      history,
      loadProvidersAndVenueProviders,
      match: {
        params: {
          offererId: 'CC',
          venueId: 'AB',
        },
      },
      providers: [
        { id: 'DD', requireProviderIdentifier: true, name: 'Cinema provider' },
        { id: 'EE', requireProviderIdentifier: true, name: 'Movies provider' },
      ],
      venueProviders: [{ id: 'AA' }, { id: 'BB' }],
    }
  })

  it('should match snapshot', () => {
    // when
    const wrapper = shallow(<VenueProvidersManager {...props} />)

    // then
    expect(wrapper).toMatchSnapshot()
  })

  it('should initialize VenueProvidersManager component with default state', () => {
    // when
    const wrapper = shallow(<VenueProvidersManager {...props} />)

    // then
    expect(wrapper.state()).toStrictEqual({
      isCreationMode: false,
      isLoadingMode: false,
      isProviderSelected: false,
      providerId: null,
      providerSelectedIsAllocine: false,
      venueIdAtOfferProviderIsRequired: true,
    })
  })

  describe('render', () => {
    it('should display a list of VenueProviderItem', () => {
      // when
      const wrapper = shallow(<VenueProvidersManager {...props} />)

      // then
      const venueProviderItem = wrapper.find(VenueProviderItem)
      expect(venueProviderItem).toHaveLength(2)
      expect(venueProviderItem.at(0).prop('venueProvider')).toStrictEqual({
        id: 'AA',
      })
      expect(venueProviderItem.at(1).prop('venueProvider')).toStrictEqual({
        id: 'BB',
      })
    })

    it('should retrieve providers and venue providers when component is mounted', () => {
      // when
      shallow(<VenueProvidersManager {...props} />)

      // then
      expect(loadProvidersAndVenueProviders).toHaveBeenCalledWith()
    })

    describe('the import button', () => {
      it('is displayed when at least one provider is given', () => {
        // when
        const wrapper = shallow(<VenueProvidersManager {...props} />)

        // then
        const importButton = wrapper.find('#add-venue-provider-btn')
        expect(importButton).toHaveLength(1)
        expect(importButton.prop('className')).toBe('button is-secondary')
        expect(importButton.prop('disabled')).toBe(false)
        expect(importButton.prop('id')).toBe('add-venue-provider-btn')
        expect(importButton.prop('onClick')).toStrictEqual(expect.any(Function))
        expect(importButton.prop('type')).toBe('button')
      })

      it('is hiden when no providers are given', () => {
        // given
        props.providers = []

        // when
        const wrapper = shallow(<VenueProvidersManager {...props} />)

        // then
        const importButton = wrapper.find('#add-venue-provider-btn')
        expect(importButton).toHaveLength(0)
      })
    })

    describe('when selecting the import button', () => {
      it('should display a select input to choose a provider', () => {
        // given
        const wrapper = shallow(<VenueProvidersManager {...props} />)
        const addOfferBtn = wrapper.find('#add-venue-provider-btn')

        // when
        addOfferBtn.simulate('click')

        // then
        const selectButton = wrapper.find('#select-source')
        expect(selectButton).toHaveLength(1)
        const selectButtonOptions = wrapper.find('#provider-options option')
        expect(selectButtonOptions).toHaveLength(3)
        expect(selectButtonOptions.at(0).text()).toStrictEqual('Choix de la source')
        expect(selectButtonOptions.at(1).text()).toStrictEqual('Cinema provider')
        expect(selectButtonOptions.at(2).text()).toStrictEqual('Movies provider')
      })
    })
  })

  describe('handleChange', () => {
    let input
    let onChange

    beforeEach(() => {
      onChange = jest.fn()
      input = {
        onChange,
      }
    })

    it('should display the allocine form when the user choose Allocine', () => {
      // given
      props.providers = [{ id: 'EM', name: 'Allociné' }]
      const chooseAllocineEvent = {
        target: {
          value: '{"id":"EM","name":"Allociné"}',
        },
      }
      const wrapper = shallow(<VenueProvidersManager {...props} />)

      // when
      wrapper.find('#add-venue-provider-btn').simulate('click')
      wrapper.find('#provider-options').simulate('change', chooseAllocineEvent)

      // then
      const allocineProviderForm = wrapper.find(AllocineProviderFormContainer)
      expect(allocineProviderForm).toHaveLength(1)
    })

    it('should update state values when selected option is valid and different from default value', () => {
      // given
      const event = {
        target: {
          value: '{"id":"AE", "requireProviderIdentifier": true}',
        },
      }
      const wrapper = shallow(<VenueProvidersManager {...props} />)

      // when
      wrapper.instance().handleChange(event, input)

      // then
      expect(wrapper.state('isProviderSelected')).toBe(true)
      expect(wrapper.state('venueIdAtOfferProviderIsRequired')).toBe(true)
    })

    it('should update providerSelectedIsAllocine values when Allocine is selected', () => {
      // given
      const event = {
        target: {
          value: '{"id":"EM","name":"Allociné"}',
        },
      }
      const wrapper = shallow(<VenueProvidersManager {...props} />)

      // when
      wrapper.instance().handleChange(event, input)

      // then
      expect(wrapper.state('providerSelectedIsAllocine')).toBe(true)
    })
  })
})
