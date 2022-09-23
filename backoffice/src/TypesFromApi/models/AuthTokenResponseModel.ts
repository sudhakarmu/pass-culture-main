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
 * @interface AuthTokenResponseModel
 */
export interface AuthTokenResponseModel {
  /**
   *
   * @type {string}
   * @memberof AuthTokenResponseModel
   */
  token: string
}

export function AuthTokenResponseModelFromJSON(
  json: any
): AuthTokenResponseModel {
  return AuthTokenResponseModelFromJSONTyped(json, false)
}

export function AuthTokenResponseModelFromJSONTyped(
  json: any,
  ignoreDiscriminator: boolean
): AuthTokenResponseModel {
  if (json === undefined || json === null) {
    return json
  }
  return {
    token: json['token'],
  }
}

export function AuthTokenResponseModelToJSON(
  value?: AuthTokenResponseModel | null
): any {
  if (value === undefined) {
    return undefined
  }
  if (value === null) {
    return null
  }
  return {
    token: value.token,
  }
}