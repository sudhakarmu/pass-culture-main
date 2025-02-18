import React from 'react'
import { Route, Routes } from 'react-router-dom-v5-compat'

import { SignupJourneyFormLayout } from 'components/SignupJourneyFormLayout'
import { SignupJourneyContextProvider } from 'context/SignupJourneyContext'
import { Activity } from 'screens/SignupJourneyForm/Activity'

const SignupJourneyRoutes = () => {
  return (
    <SignupJourneyContextProvider>
      <SignupJourneyFormLayout>
        <Routes>
          <Route
            path={'/authentification'}
            element={<div>Authentification</div>}
          />
          <Route path={'/activite'} element={<Activity />} />
          <Route path={'/validation'} element={<div>Validation</div>} />
        </Routes>
      </SignupJourneyFormLayout>
    </SignupJourneyContextProvider>
  )
}

export default SignupJourneyRoutes
