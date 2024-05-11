from exceptions.APIExceptions import *


def check_answer(status_code):
    if status_code == 400:
        raise IncorrectDataError
    elif status_code == 401:
        raise NonAuthorizedError
    elif status_code == 403:
        raise APIError
    elif status_code == 404:
        raise UnsuccessfulSearchError
    elif status_code == 406:
        raise ResourceCouldNotBeShownError
    elif status_code == 413:
        raise TooBigFileError
    elif status_code == 423:
        raise OnlyCanShowError
    elif status_code == 429:
        raise TooManyRequestsError
    elif status_code == 503:
        raise ServiceUnavailableError
    elif status_code == 415:
        raise NotGoodFormatError
    elif status_code == 409:
        raise PathExistsError
    elif status_code == 507:
        raise NotEmptySpaceError
    elif status_code == 412:
        raise WfolioError
