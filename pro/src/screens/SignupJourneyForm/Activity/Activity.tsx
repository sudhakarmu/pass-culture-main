import { FormikProvider, useFormik } from 'formik'
import React from 'react'

import FormLayout from 'components/FormLayout'
import { SIGNUP_STEP_IDS } from 'components/SignupJourneyBreadcrumb/constants'
import { FORM_ERROR_MESSAGE } from 'core/shared'
import { useGetVenueTypes } from 'core/Venue/adapters/getVenueTypeAdapter'
import { useNavigate } from 'hooks'
import useNotification from 'hooks/useNotification'
import Spinner from 'ui-kit/Spinner/Spinner'

import { ActionBar } from '../ActionBar'

import ActivityForm, { IActivityFormValues } from './ActivityForm'
import { DEFAULT_ACTIVITY_FORM_VALUES } from './constants'
import { validationSchema } from './validationSchema'

const Activity = (): JSX.Element => {
  const {
    isLoading: isLoadingVenueTypes,
    error: errorVenueTypes,
    data: venueTypes,
  } = useGetVenueTypes()
  const notify = useNotification()
  const navigate = useNavigate()
  // Get activity context
  const initialValues: IActivityFormValues = DEFAULT_ACTIVITY_FORM_VALUES

  const handleNextStep = () => async () => {
    if (Object.keys(formik.errors).length !== 0) {
      notify.error(FORM_ERROR_MESSAGE)
      return
    }
  }

  const onSubmitActivity = async (
    formValues: IActivityFormValues
  ): Promise<void> => {
    if (Object.keys(formik.errors).length === 0) {
      navigate('/signup/validation')
    }
  }

  const formik = useFormik({
    initialValues,
    onSubmit: onSubmitActivity,
    validationSchema,
    enableReinitialize: true,
  })

  const handlePreviousStep = () => {
    navigate('/signup/authentification')
  }

  if (isLoadingVenueTypes) {
    return <Spinner />
  }

  if (errorVenueTypes) {
    return <></>
  }

  return (
    <FormLayout>
      <FormikProvider value={formik}>
        <form onSubmit={formik.handleSubmit} data-testid="signup-activity-form">
          <ActivityForm venueTypes={venueTypes ?? []} />
          <ActionBar
            onClickPrevious={handlePreviousStep}
            onClickNext={handleNextStep()}
            step={SIGNUP_STEP_IDS.ACTIVITY}
            isDisabled={formik.isSubmitting}
          />
        </form>
      </FormikProvider>
    </FormLayout>
  )
}

export default Activity