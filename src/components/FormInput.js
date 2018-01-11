import React, { Component } from 'react'
import { connect } from 'react-redux'

import { assignForm } from '../reducers/form'

class FormInput extends Component {
  onChange = ({ target: { value } }) => {
    const { assignForm, name } = this.props
    assignForm({ [name]: value })
  }
  render () {
    const { className, defaultValue, placeholder, type } = this.props
    return <input className={className || 'input'}
      defaultValue={defaultValue}
      onChange={this.onChange}
      placeholder={placeholder}
      type={type} />
  }
}

export default connect(null, { assignForm })(FormInput)
