import React, { Component } from 'react'
import { NavLink } from 'react-router-dom'
import { compose } from 'redux'
import { withRouter } from 'react-router'
import { connect } from 'react-redux'

import OccasionItem from '../OccasionItem'
import Icon from '../layout/Icon'
import SearchInput from '../layout/SearchInput'
import PageWrapper from '../layout/PageWrapper'
import { showModal } from '../../reducers/modal'
import { requestData } from '../../reducers/data'
import createOccasionsSelector from '../../selectors/createOccasions'
import createOffererSelector from '../../selectors/createOfferer'
import createSearchSelector from '../../selectors/createSearch'
import createVenueSelector from '../../selectors/createVenue'
import { occasionNormalizer } from '../../utils/normalizers'

class OccasionsPage extends Component {

  handleDataRequest = (handleSuccess, handleError) => {
    const {
      requestData,
      user
    } = this.props
    user && requestData(
      'GET',
      'occasions',
      {
        handleSuccess,
        handleError,
        normalizer: occasionNormalizer
      }
    )
    requestData('GET', 'types')
  }

  render() {
    const {
      occasions,
      offerer,
      venue
    } = this.props

    return (
      <PageWrapper name="offers" handleDataRequest={this.handleDataRequest}>
        <div className="section">
          <NavLink to={`/offres/nouveau`} className='button is-primary is-medium is-pulled-right'>
            <span className='icon'><Icon svg='ico-offres-w' /></span>
            <span>Créer une offre</span>
          </NavLink>
          <h1 className='pc-title'>
            Vos offres
          </h1>
        </div>
        <div className='section'>
          <label className="label">Rechercher une offre :</label>
          <div className="field is-grouped">
            <p className="control is-expanded">
              <SearchInput
                collectionNames={["events", "things"]}
                config={{
                  isMergingArray: false,
                  key: 'searchedOccasions'
                }}
                isLoading
              />
            </p>
            <p className="control">
              <button className='button is-primary is-outlined is-medium'>OK</button>
              {' '}
              <button className='button is-secondary is-medium'>&nbsp;<Icon svg='ico-filter' />&nbsp;</button>
            </p>
          </div>
        </div>

        <div className='section'>
          {
            offerer
              ? (
                <p>
                  structure: {offerer.name}
                </p>
              )
              : venue && (
                <p>
                  lieu: {venue.name}
                </p>
              )
          }
        </div>

        {
          <div className='section load-wrapper'>
            <ul className='occasions-list pc-list'>
              {
                occasions.map(o =>
                  <OccasionItem key={o.id} occasion={o} />)
              }
            </ul>
          </div>
        }
      </PageWrapper>
    )
  }
}


const occasionsSelector = createOccasionsSelector()
const offererSelector = createOffererSelector()
const searchSelector = createSearchSelector()
const venueSelector = createVenueSelector()

export default compose(
  withRouter,
  connect(
    (state, ownProps) => {
      const { structure, lieu } = searchSelector(state, ownProps.location.search)
      return {
        occasions: occasionsSelector(state, structure, lieu),
        offerer: offererSelector(state, structure),
        user: state.user,
        venue: venueSelector(state, lieu)
      }
    },
    { showModal, requestData }
  )
)(OccasionsPage)
