import "@elastic/react-search-ui-views/lib/styles/styles.css"
import {
  SearchBox,
  SearchProvider,
  WithSearch,
} from "@elastic/react-search-ui"
import AppSearchAPIConnector from "@elastic/search-ui-app-search-connector"
import * as React from "react"
import { useCallback } from "react"

import { Notification } from "app/components/Layout/Notification/Notification"
import { APP_SEARCH_ENDPOINT, APP_SEARCH_KEY } from "utils/config"
import { RESULT_FIELDS } from "utils/search"
import { Role } from "utils/types"

import { Offers } from "./Offers/Offers"

const connector = new AppSearchAPIConnector({
  searchKey: APP_SEARCH_KEY,
  engineName: "offers",
  endpointBase: APP_SEARCH_ENDPOINT,
})
const configurationOptions = {
  searchQuery: {
    result_fields: RESULT_FIELDS,
    filters: [{ field: "is_educational", values: [1] }],
  },
  trackUrlState: false,
  alwaysSearchOnInitialLoad: true,
}

export const OffersSearch = ({
  notify,
  userRole,
}: {
  notify: (notification: Notification) => void;
  userRole: Role;
}): JSX.Element => {
  const mapContextToProps = useCallback(
    ({
      autocompletedResults,
      autocompletedSuggestions,
      trackAutocompleteClickThrough,
      searchTerm,
      setSearchTerm,
      results,
    }) => ({
      autocompletedResults,
      autocompletedSuggestions,
      trackAutocompleteClickThrough,
      searchTerm,
      setSearchTerm,
      results,
    }),
    []
  )

  const inputView = useCallback(
    ({ getAutocomplete, getInputProps, getButtonProps }) => (
      <>
        <div className="sui-search-box__wrapper">
          <input
            {...getInputProps({
              placeholder:
                "Nom de l'offre, du lieu ou de la catégorie (Films, Visites, Conférences, Spectacles, Cours, Musique)",
            })}
          />
          {getAutocomplete()}
        </div>
        <input
          {...getButtonProps({
            value: "Rechercher",
          })}
        />
      </>
    ),
    []
  )

  return (
    <>
      <h2>
        Rechercher une offre
      </h2>
      <SearchProvider
        config={{
          apiConnector: connector,
          ...configurationOptions,
        }}
      >
        <WithSearch mapContextToProps={mapContextToProps}>
          {({
            autocompletedResults,
            autocompletedSuggestions,
            trackAutocompleteClickThrough,
            searchTerm,
            setSearchTerm,
            results,
          }) => {
            return (
              <>
                <SearchBox
                  autocompletedResults={autocompletedResults}
                  autocompletedSuggestions={autocompletedSuggestions}
                  inputView={inputView}
                  searchTerm={searchTerm}
                  setSearchTerm={setSearchTerm}
                  trackAutocompleteClickThrough={trackAutocompleteClickThrough}
                />
                <Offers
                  notify={notify}
                  results={results}
                  userRole={userRole}
                />
              </>
            )
          }}
        </WithSearch>
      </SearchProvider>
    </>
  )
}
