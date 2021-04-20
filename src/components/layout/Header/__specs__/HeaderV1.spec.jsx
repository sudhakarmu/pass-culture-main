import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import React from 'react'
import { Provider } from 'react-redux'
import { MemoryRouter } from 'react-router'

import { configureTestStore } from 'store/testUtils'

import * as constants from '../_constants'
import HeaderV1 from '../HeaderV1'

const renderHeader = props => {
  const stubStore = configureTestStore()

  return render(
    <Provider store={stubStore}>
      <MemoryRouter>
        <HeaderV1 {...props} />
      </MemoryRouter>
    </Provider>
  )
}

describe('navigation menu', () => {
  let props
  beforeEach(() => {
    props = {
      dispatch: jest.fn(),
      name: 'Utilisateur',
      offerers: [{ id: '1' }],
    }
  })

  describe('should pluralize Offerer menu link', () => {
    it('should display Structure juridique for a single offerer', () => {
      // when
      renderHeader(props)

      // then
      const singularOffererLink = screen.queryByText('Structure juridique')
      const pluralOffererLink = screen.queryByText('Structures juridiques')
      expect(singularOffererLink).toBeInTheDocument()
      expect(singularOffererLink.closest('a')).toHaveAttribute('href', '/structures')
      expect(pluralOffererLink).not.toBeInTheDocument()
    })

    it('should display Structures juridiques for multiple offerers', () => {
      // given
      props.offerers = [{}, {}]

      // when
      renderHeader(props)

      // then
      const singularOffererLink = screen.queryByText('Structure juridique')
      const pluralOffererLink = screen.queryByText('Structures juridiques')
      expect(singularOffererLink).not.toBeInTheDocument()
      expect(pluralOffererLink).toBeInTheDocument()
      expect(pluralOffererLink.closest('a')).toHaveAttribute('href', '/structures')
    })
  })

  describe('help link', () => {
    it('should display a "help" link in the header', () => {
      // when
      renderHeader(props)

      // then
      const helpLink = screen.queryByText('Aide')
      expect(helpLink.closest('a')).toHaveAttribute(
        'href',
        'https://aide.passculture.app'
      )
      expect(helpLink.closest('a')).toHaveAttribute('target', '_blank')
    })
  })

  it('should have link to Guichet', () => {
    // Given
    renderHeader(props)

    // When
    const guichetLink = screen.getByText('Guichet')

    // Then
    expect(guichetLink.closest('a')).toHaveAttribute('href', '/guichet')
  })

  it('should have link to Offres', () => {
    // Given
    renderHeader(props)

    // When
    const guichetLink = screen.getByText('Offres')

    // Then
    expect(guichetLink.closest('a')).toHaveAttribute('href', '/offres')
  })

  it('should have link to Profil', () => {
    // Given
    renderHeader(props)

    // When
    const guichetLink = screen.getByText('Profil')

    // Then
    expect(guichetLink.closest('a')).toHaveAttribute('href', '/profil')
  })

  it('should have link to Remboursements', () => {
    // Given
    renderHeader(props)

    // When
    const guichetLink = screen.getByText('Remboursements')

    // Then
    expect(guichetLink.closest('a')).toHaveAttribute('href', '/remboursements')
  })

  it('should have link to Déconnexion', () => {
    // When
    renderHeader(props)

    // Then
    const logOutButton = screen.queryByText('Déconnexion')
    expect(logOutButton).toBeInTheDocument()
  })

  it('should have link to Styleguide when is enabled', () => {
    // Given
    // eslint-disable-next-line
    constants.STYLEGUIDE_ACTIVE = true
    renderHeader(props)

    // Then
    expect(screen.queryByText('Styleguide')).toBeInTheDocument()
  })

  it('should not have link to Styleguide when is disabled', () => {
    // given
    // eslint-disable-next-line
    constants.STYLEGUIDE_ACTIVE = false

    // When
    renderHeader(props)

    // Then
    expect(screen.queryByText('Styleguide')).not.toBeInTheDocument()
  })

  // reste : les éléments conditionnels (Styleguide)
  // devnote : comment tester que les élements du menu secondaire s'affichent au hover
})
