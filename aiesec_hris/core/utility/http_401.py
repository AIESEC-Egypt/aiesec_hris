from django.http import HttpResponse


class Http401(HttpResponse):
    """
    Http 401 unauthorized response
    """
    status_code = 401
