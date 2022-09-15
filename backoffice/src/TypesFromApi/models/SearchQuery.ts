/* tslint:disable */
/* eslint-disable */
/**
 * pass Culture backoffice API
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1
 *
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime'
/**
 *
 * @export
 * @interface SearchQuery
 */
export interface SearchQuery {
  /**
   *
   * @type {number}
   * @memberof SearchQuery
   */
  page?: number | null
  /**
   *
   * @type {number}
   * @memberof SearchQuery
   */
  perPage?: number | null
  /**
   *
   * @type {string}
   * @memberof SearchQuery
   */
  q: string
  /**
   *
   * @type {string}
   * @memberof SearchQuery
   */
  sort?: string | null
}

export function SearchQueryFromJSON(json: any): SearchQuery {
  return SearchQueryFromJSONTyped(json, false)
}

export function SearchQueryFromJSONTyped(
  json: any,
  ignoreDiscriminator: boolean
): SearchQuery {
  if (json === undefined || json === null) {
    return json
  }
  return {
    page: !exists(json, 'page') ? undefined : json['page'],
    perPage: !exists(json, 'perPage') ? undefined : json['perPage'],
    q: json['q'],
    sort: !exists(json, 'sort') ? undefined : json['sort'],
  }
}

export function SearchQueryToJSON(value?: SearchQuery | null): any {
  if (value === undefined) {
    return undefined
  }
  if (value === null) {
    return null
  }
  return {
    page: value.page,
    perPage: value.perPage,
    q: value.q,
    sort: value.sort,
  }
}
