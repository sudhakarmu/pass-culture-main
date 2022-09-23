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
 * @interface GetBeneficiaryCreditResponseModel
 */
export interface GetBeneficiaryCreditResponseModel {
  /**
   *
   * @type {Date}
   * @memberof GetBeneficiaryCreditResponseModel
   */
  dateCreated?: Date | null
  /**
   *
   * @type {number}
   * @memberof GetBeneficiaryCreditResponseModel
   */
  initialCredit: number
  /**
   *
   * @type {number}
   * @memberof GetBeneficiaryCreditResponseModel
   */
  remainingCredit: number
  /**
   *
   * @type {number}
   * @memberof GetBeneficiaryCreditResponseModel
   */
  remainingDigitalCredit: number
}

export function GetBeneficiaryCreditResponseModelFromJSON(
  json: any
): GetBeneficiaryCreditResponseModel {
  return GetBeneficiaryCreditResponseModelFromJSONTyped(json, false)
}

export function GetBeneficiaryCreditResponseModelFromJSONTyped(
  json: any,
  ignoreDiscriminator: boolean
): GetBeneficiaryCreditResponseModel {
  if (json === undefined || json === null) {
    return json
  }
  return {
    dateCreated: !exists(json, 'dateCreated')
      ? undefined
      : json['dateCreated'] === null
      ? null
      : new Date(json['dateCreated']),
    initialCredit: json['initialCredit'],
    remainingCredit: json['remainingCredit'],
    remainingDigitalCredit: json['remainingDigitalCredit'],
  }
}

export function GetBeneficiaryCreditResponseModelToJSON(
  value?: GetBeneficiaryCreditResponseModel | null
): any {
  if (value === undefined) {
    return undefined
  }
  if (value === null) {
    return null
  }
  return {
    dateCreated:
      value.dateCreated === undefined
        ? undefined
        : value.dateCreated === null
        ? null
        : value.dateCreated.toISOString(),
    initialCredit: value.initialCredit,
    remainingCredit: value.remainingCredit,
    remainingDigitalCredit: value.remainingDigitalCredit,
  }
}