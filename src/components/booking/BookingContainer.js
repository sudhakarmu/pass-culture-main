<<<<<<< HEAD
import get from 'lodash.get'
import { connect } from 'react-redux'
import { selectBookables } from '../../selectors/selectBookables'
import { selectBookingById } from '../../selectors/selectBookings'
import { currentRecommendationSelector } from '../../selectors'
=======
/* eslint
  react/jsx-one-expression-per-line: 0 */
import get from 'lodash.get'
import { connect } from 'react-redux'

import { selectBookables } from '../../selectors/selectBookables'
import { selectBookingById } from '../../selectors/selectBookings'
import currentRecommendationSelector from '../../selectors/currentRecommendation'
>>>>>>> (PC-1723): Rename last usage of eventOrThing and event / thing
import Booking from './Booking'

export const mapStateToProps = (state, { match }) => {
  const { offerId, mediationId, view, bookingId } = match.params
  const recommendation = currentRecommendationSelector(
    state,
    offerId,
    mediationId
  )

  const isEvent = get(recommendation, 'offer.isEvent')
  const bookables = selectBookables(state, recommendation, match)
  const booking = selectBookingById(state, bookingId)
  const isCancelled = view === 'cancelled'

  return {
    bookables,
    booking,
    isCancelled,
    isEvent,
    recommendation,
  }
}

export default connect(mapStateToProps)(Booking)
