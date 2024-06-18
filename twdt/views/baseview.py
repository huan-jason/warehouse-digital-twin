from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .utils import api_key_check


@method_decorator(csrf_exempt, name="dispatch")
class BaseView(View):

    def _get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        raise NotImplementedError

    def _post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        raise NotImplementedError

    def _put(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        raise NotImplementedError

    def get(self, request: HttpRequest, *args: Any, response_type: str = "", **kwargs: Any) -> HttpResponse | JsonResponse:
        if not response_type and not request.user.is_authenticated:
            url: str = reverse("login")
            return redirect(f"{url}?next=/")

        return self._get(request, *args, response_type=response_type, **kwargs)

    @api_key_check
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        return self._post(request, *args, **kwargs)

    @api_key_check
    def put(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        return self._put(request, *args, **kwargs)


