class NonAuthorizedError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'Не авторизован'


class IncorrectDataError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'Некорректные данные.'


class APIError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return ('API недоступно. Ваши файлы занимают больше места, '
                'чем у вас есть. Удалите лишнее или увеличьте объём Диска.')


class UnsuccessfulSearchError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'Не удалось найти запрошенный ресурс.'


class ResourceCouldNotBeShownError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'Ресурс не может быть представлен в запрошенном формате.'


class TooBigFileError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'Загрузка файла недоступна. Файл слишком большой.'


class OnlyCanShowError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'Технические работы. Сейчас можно только просматривать и скачивать файлы.'


class TooManyRequestsError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'Слишком много запросов.'


class ServiceUnavailableError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'Сервис недоступен.'


class NotGoodFormatError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'Неподдерживаемый формат данных в теле запроса.'


class PathExistsError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'Путь уже существует.'


class NotEmptySpaceError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'Недостаточно свободного места.'


class WfolioError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'Перемещение папки с проектом Wfolio в чужую ОП не поддерживается.'
