/*
 * @debt complexity "Gaël: file nested too deep in directory structure"
 */

import '@testing-library/jest-dom'
import { screen } from '@testing-library/react'

import { renderOffer } from 'components/pages/Offers/Offer/__specs__/render'
import { offerFactory } from 'utils/apiFactories'
import { loadFakeApiOffer } from 'utils/fakeApi'

jest.mock('utils/config', () => {
  return {
    WEBAPP_URL: 'http://localhost',
  }
})

describe('confirmation page', () => {
  it('should display the rights information when offer is draft', async () => {
    // Given
    const offer = offerFactory({ name: 'mon offre', status: 'DRAFT' })
    loadFakeApiOffer(offer)

    // When
    await renderOffer({
      pathname: `/offre/${offer.id}/individuel/confirmation`,
    })

    // Then
    expect(screen.queryByText('active')).not.toBeInTheDocument()
    expect(
      screen.getByText('Offre créée !', { selector: 'h2' })
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        'Votre offre est désormais disponible à la réservation sur l’application pass Culture.',
        { selector: 'p' }
      )
    ).toBeInTheDocument()
    expect(
      screen.getByText('Prévisualiser dans l’app', { selector: 'a' })
    ).toHaveAttribute('href', `http://localhost/offre/${offer.nonHumanizedId}`)
    expect(
      screen.getByText('Créer une nouvelle offre', { selector: 'a' })
    ).toHaveAttribute('href', '/offre/creation/individuel')
  })

  it('should display the rights information when offer is pending', async () => {
    // Given
    const offer = offerFactory({ name: 'mon offre', status: 'PENDING' })
    loadFakeApiOffer(offer)

    // When
    await renderOffer({
      pathname: `/offre/${offer.id}/individuel/confirmation`,
    })

    // Then
    expect(screen.queryByText('active')).not.toBeInTheDocument()
    expect(
      screen.getByText('Offre en cours de validation', { selector: 'h2' })
    ).toBeInTheDocument()
    expect(
      screen.queryByText(content =>
        content.startsWith(
          'Votre offre est en cours de validation par l’équipe pass Culture'
        )
      )
    ).toBeInTheDocument()
    expect(
      screen.getByText('Prévisualiser dans l’app', { selector: 'a' })
    ).toHaveAttribute('href', `http://localhost/offre/${offer.nonHumanizedId}`)
    expect(
      screen.getByText('Créer une nouvelle offre', { selector: 'a' })
    ).toHaveAttribute('href', '/offre/creation/individuel')
  })

  it('should redirect to offer edition when the offer is not a draft', async () => {
    // Given
    const offer = offerFactory({ name: 'mon offre', status: 'ACTIVE' })
    loadFakeApiOffer(offer)

    // When
    await renderOffer({
      pathname: [
        `/offres/${offer.id}/edition`,
        `/offre/${offer.id}/individuel/confirmation`,
      ],
    })

    // Then
    expect(screen.getByText('Éditer une offre')).toBeInTheDocument()
  })

  it('should land to offer edition when you come from an offerer', async () => {
    // Given
    const offer = offerFactory({ name: 'mon offre', status: 'DRAFT' })
    loadFakeApiOffer(offer)

    // When
    await renderOffer({
      pathname: [`/offre/${offer.id}/individuel/confirmation`],
      search: '?structure=OFFERER1&lieu=VENUE1',
    })

    // Then
    expect(
      screen.getByText('Créer une nouvelle offre', { selector: 'a' })
    ).toHaveAttribute(
      'href',
      '/offre/creation/individuel?structure=OFFERER1&lieu=VENUE1'
    )
  })
})
