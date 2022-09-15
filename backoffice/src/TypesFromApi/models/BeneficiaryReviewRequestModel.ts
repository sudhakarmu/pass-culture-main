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
import {
  FraudReviewStatus,
  FraudReviewStatusFromJSON,
  FraudReviewStatusFromJSONTyped,
  FraudReviewStatusToJSON,
} from './index'

/**
 *
 * @export
 * @interface BeneficiaryReviewRequestModel
 */
export interface BeneficiaryReviewRequestModel {
  /**
   *
   * @type {string}
   * @memberof BeneficiaryReviewRequestModel
   */
  eligibility?: string | null
  /**
   *
   * @type {string}
   * @memberof BeneficiaryReviewRequestModel
   */
  reason: string
  /**
   *
   * @type {FraudReviewStatus}
   * @memberof BeneficiaryReviewRequestModel
   */
  review: FraudReviewStatus
}

export function BeneficiaryReviewRequestModelFromJSON(
  json: any
): BeneficiaryReviewRequestModel {
  return BeneficiaryReviewRequestModelFromJSONTyped(json, false)
}

export function BeneficiaryReviewRequestModelFromJSONTyped(
  json: any,
  ignoreDiscriminator: boolean
): BeneficiaryReviewRequestModel {
  if (json === undefined || json === null) {
    return json
  }
  return {
    eligibility: !exists(json, 'eligibility') ? undefined : json['eligibility'],
    reason: json['reason'],
    review: FraudReviewStatusFromJSON(json['review']),
  }
}

export function BeneficiaryReviewRequestModelToJSON(
  value?: BeneficiaryReviewRequestModel | null
): any {
  if (value === undefined) {
    return undefined
  }
  if (value === null) {
    return null
  }
  return {
    eligibility: value.eligibility,
    reason: value.reason,
    review: FraudReviewStatusToJSON(value.review),
  }
}
