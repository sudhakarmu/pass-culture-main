import { useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom-v5-compat'

import { api } from 'apiClient/api'
import { getError, isErrorAPIError } from 'apiClient/helpers'
import useCurrentUser from 'hooks/useCurrentUser'
import useNotification from 'hooks/useNotification'
import { campaignTracker } from 'tracking/mediaCampaignsTracking'

type Params = { token: string }

const SignupValidation = (): null => {
  const { token } = useParams<Params>()
  const { currentUser } = useCurrentUser()
  const navigate = useNavigate()
  useEffect(() => {
    campaignTracker.signUpValidation()
  }, [])
  const notify = useNotification()

  useEffect(() => {
    const validateTokenAndRedirect = async () => {
      if (currentUser?.id) {
        navigate('/')
      } else if (token) {
        try {
          await api.validateUser(token)
          notify.success(
            'Votre compte a été créé. Vous pouvez vous connecter avec les identifiants que vous avez choisis.'
          )
        } catch (error) {
          if (isErrorAPIError(error)) {
            const errors = getError(error)
            notify.error(errors.global)
          }
        } finally {
          navigate('/connexion')
        }
      }
    }
    void validateTokenAndRedirect()
  }, [notify, token, currentUser?.id])

  return null
}

export default SignupValidation
