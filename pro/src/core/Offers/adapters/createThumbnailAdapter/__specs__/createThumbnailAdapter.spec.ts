import { CroppedRect } from 'react-avatar-editor'

import * as pcapi from 'repository/pcapi/pcapi'

import createThumbnailAdapter from '../createThumbnailAdapter'

describe('test createThumbnailAdapter', () => {
  let offerId: string
  let imageData: File
  let credit: string
  let cropParams: CroppedRect

  beforeEach(() => {
    offerId = 'AA'
    imageData = new File([''], 'hello.png')
    credit = 'John Do'
    cropParams = { x: 1, y: 1, width: 1, height: 1 }
  })
  it('should return success on api call success', async () => {
    jest
      .spyOn(pcapi, 'postThumbnail')
      .mockResolvedValue({ url: 'http://backend.image.url', credit: 'John Do' })
    const response = await createThumbnailAdapter({
      offerId,
      imageData,
      credit,
      cropParams,
    })
    expect(response.isOk).toBeTruthy()
  })
  it('should return error on api call error', async () => {
    jest.spyOn(pcapi, 'postThumbnail').mockRejectedValue(undefined)
    const response = await createThumbnailAdapter({
      offerId,
      imageData,
      credit,
      cropParams,
    })
    expect(response.isOk).toBeFalsy()
  })
})