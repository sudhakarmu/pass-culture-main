import React from 'react'

import HomeCard from '../HomeCard'
import Main from '../layout/Main'

const HomePage = ({ user }) => {
  return (
    <Main name="home" whiteHeader>
      <div className="home-cards columns">
        <HomeCard
          svg="ico-guichet-w"
          title="Guichet"
          text="Enregistrez les codes de réservation des porteurs du Pass (en construction, pas encore disponible)."
          navLink="/guichet"
        />
        <HomeCard
          svg="ico-offres-w"
          title="Vos offres"
          text="Créez et mettez en avant vos offres présentes sur le Pass."
          navLink="/offres"
        />
      </div>
    </Main>
  )
}

export default HomePage
