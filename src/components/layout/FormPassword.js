import get from 'lodash.get'
import classnames from 'classnames'
import PropTypes from 'prop-types'
import React, { Component } from 'react'
import { connect } from 'react-redux'

import { requestData } from '../../reducers/data'
import { randomHash } from '../../utils/random'
import Icon from './Icon'
import FormInput from './FormInput'

class FormPassword extends Component {
  constructor() {
    super()
    this.state = {
      isHidden: true,
    }
  }

  toggleHidden = e => {
    e.preventDefault()
    this.setState({
      isHidden: !this.state.isHidden
    })
  }

  render() {
    return (
      <div className="field has-addons">
        <div className="control is-expanded">
          <FormInput {...this.props} type={this.state.isHidden ? 'password' : 'text'} />
        </div>
        <div className="control">
          <button className="button is-rounded is-medium" onClick={this.toggleHidden}>
            <Icon svg={this.state.isHidden ? 'ico-eye close' : 'ico-eye'} />
            &nbsp;
          </button>
        </div>
      </div>
    )
  }
}

export default FormPassword