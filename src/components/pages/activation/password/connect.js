import { requestData } from 'pass-culture-shared'

import { getQueryStringEmail, getURLTokenParam } from '../utils'

export const mapDispatchToProps = dispatch => ({
  loginUserAfterPasswordSaveSuccess: (values, fail, success) => {
    const { email: identifier, newPassword: password } = values
    const options = {
      body: { identifier, password },
      handleFail: fail,
      handleSuccess: success,
    }
    const requestMethod = 'POST'
    const requestPath = 'users/signin'
    dispatch(requestData(requestMethod, requestPath, options))
  },

  sendActivationPasswordForm: (values, fail, success) => {
    // NOTE: on retourne une promise au formulaire
    // pour pouvoir gérer les erreurs de l'API
    // directement dans les champs du formulaire
    const formSubmitPromise = new Promise(resolve => {
      const options = {
        body: { ...values },
        handleFail: fail(resolve),
        handleSuccess: success(resolve, values),
      }
      const requestMethod = 'POST'
      const requestPath = 'users/new-password'
      dispatch(requestData(requestMethod, requestPath, options))
    })
    return formSubmitPromise
  },
})

export const mapStateToProps = (state, { location, match }) => {
  const email = getQueryStringEmail(location)
  const token = getURLTokenParam(match)
  const initialValues = { email, token }
  return {
    initialValues,
  }
}
