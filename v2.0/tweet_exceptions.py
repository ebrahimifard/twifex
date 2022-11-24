
class PhotoDownloadError(ValueError):
    pass


class PhotoNotFoundInSpecifiedUrl(PhotoDownloadError):
    pass


class OtherPhotoError(PhotoDownloadError):
    pass


class VideoDownloadError(ValueError):
    pass


class VideoNotFoundInSpecifiedUrl(VideoDownloadError):
    pass


class OtherVideoError(VideoDownloadError):
    pass


class GifDownloadError(ValueError):
    pass


class GifNotFoundInSpecifiedUrl(GifDownloadError):
    pass


class OtherGifError(GifDownloadError):
    pass


class RetweetObjectNotAvailable(ValueError):
    pass


class QuoteTweetObjectNotAvailable(ValueError):
    pass


class TweetLengthZero(ZeroDivisionError):
    pass


class ZeroUppercaseCharacters(ZeroDivisionError):
    pass


class ZeroLowercaseCharacters(ZeroDivisionError):
    pass




