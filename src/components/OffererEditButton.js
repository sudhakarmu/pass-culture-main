import React, { Component } from 'react'
import { connect } from 'react-redux'

import OffererForm from './OffererForm'
import { showModal } from '../reducers/modal'

class OffererEditButton extends Component {
  onClick = () => {
    const { showModal } = this.props
    showModal(<OffererForm />)
  }

  render() {
    return (
      <button
        className="button is-primary level-item"
        onClick={this.onClick}
      >
        Mes sources
      </button>
    )
  }
}

export default connect(
  null,
  { showModal }
)(OffererEditButton)
