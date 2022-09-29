import React from 'react'

import { ReactComponent as TrashFilledIcon } from 'icons/ico-trash-filled.svg'
import FormLayout from 'new_components/FormLayout'
import { NOTIFICATIONS_EMAIL_LABEL } from 'screens/OfferEducational/constants/labels'
import { TextInput } from 'ui-kit'
import TooltipWrapper from 'ui-kit/TooltipWrapper'

import styles from './EmailInputRow.module.scss'

interface IEmailInputRowProps {
  disableForm: boolean
  displayTrash?: boolean
  name: string
  onDelete?: () => void
}

const EmailInputRow = ({
  disableForm,
  displayTrash = true,
  name,
  onDelete,
}: IEmailInputRowProps) => {
  return (
    <FormLayout.Row inline>
      <TextInput
        label={NOTIFICATIONS_EMAIL_LABEL}
        name={name}
        disabled={disableForm}
        className={styles['notification-mail-input']}
      />
      {displayTrash && (
        <TooltipWrapper title="Supprimer l'email" delay={0}>
          <TrashFilledIcon
            onClick={onDelete}
            className={styles['trash-icon']}
            title="Supprimer l'email"
          />
        </TooltipWrapper>
      )}
    </FormLayout.Row>
  )
}

export default EmailInputRow