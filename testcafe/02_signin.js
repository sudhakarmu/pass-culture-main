import { Selector } from 'testcafe'
import getPageUrl from './helpers/getPageUrl'
import { fetchSandbox } from './helpers/sandboxes'
import { ROOT_PATH } from '../src/utils/config'

const userId = '#user-identifier'
const passId = '#user-password'
const errorClass = '.pc-error-message'
const userPassword = Selector(passId)
const userIdentifier = Selector(userId)
const identifierErrors = Selector(`${userId}-error`).find(errorClass)
const signInButton = Selector('#signin-submit-button')

fixture("02_01 SignIn | J'ai un compte et je me connecte")
  .page(`${ROOT_PATH}connexion`)
  .beforeEach(async t => {
    t.ctx.sandbox = await fetchSandbox(
      'webapp_02_signin',
      'get_existing_webapp_validated_user_with_has_filled_cultural_survey'
    )
  })

test("J'ai un compte valide, je suis redirigé·e vers la page /decouverte sans erreurs", async t => {
  // given
  const { user } = t.ctx.sandbox
  const { email, password } = user
  await t
    .typeText(
      userIdentifier,
      email,
      // https://github.com/DevExpress/testcafe/issues/3865
      { paste: true }
    )
    .typeText(userPassword, password)

  // when
  await t.click(signInButton).wait(1000)

  // then
  await t.expect(identifierErrors.count).eql(0)
  await t.expect(getPageUrl()).contains('/decouverte')
})
