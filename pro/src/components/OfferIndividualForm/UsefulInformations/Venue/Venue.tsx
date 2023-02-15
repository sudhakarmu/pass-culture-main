import { useFormikContext } from 'formik'
import React from 'react'

import FormLayout from 'components/FormLayout'
import { IOfferIndividualFormValues } from 'components/OfferIndividualForm'
import { TOffererName } from 'core/Offerers/types'
import { TOfferIndividualVenue } from 'core/Venue/types'
import { Select } from 'ui-kit'

import { buildOffererOptions, buildVenueOptions } from './utils'

export interface IVenueProps {
  offererNames: TOffererName[]
  venueList: TOfferIndividualVenue[]
  readOnlyFields?: string[]
}

const Venue = ({
  offererNames,
  venueList,
  readOnlyFields = [],
}: IVenueProps): JSX.Element => {
  const { values, setFieldValue } =
    useFormikContext<IOfferIndividualFormValues>()
  const { isDisabled: isOffererDisabled, offererOptions } =
    buildOffererOptions(offererNames)

  const { isDisabled: isVenueDisabled, venueOptions } = buildVenueOptions(
    values.offererId,
    venueList
  )

  const onVenueChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newVenue = venueList.find(v => v.id === event.target.value)

    if (!newVenue) {
      return
    }
    setFieldValue('isVenueVirtual', newVenue.isVirtual)
    setFieldValue('withdrawalDetails', newVenue?.withdrawalDetails || '')

    // update offer accessibility from venue when venue accessibility is defined.
    // set accessibility value after isVenueVirtual and withdrawalDetails otherwise the error message doesn't hide
    Object.values(newVenue.accessibility).includes(true) &&
      setFieldValue('accessibility', newVenue.accessibility)
  }

  return (
    <>
      <FormLayout.Row>
        <Select
          disabled={isOffererDisabled || readOnlyFields.includes('offererId')}
          label="Structure"
          name="offererId"
          options={offererOptions}
        />
      </FormLayout.Row>
      <FormLayout.Row>
        <Select
          disabled={isVenueDisabled || readOnlyFields.includes('venueId')}
          label="Lieu"
          name="venueId"
          options={venueOptions}
          onChange={onVenueChange}
        />
      </FormLayout.Row>
    </>
  )
}

export default Venue
