from typing import Any, Protocol, TypedDict

from django.http import HttpRequest, HttpResponse, JsonResponse


class Coordinates(TypedDict):
    x: float
    y: float
    z: float
