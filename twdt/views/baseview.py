from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .api_key_check import api_key_check


@method_decorator(csrf_exempt, name="dispatch")
class BaseView(View):

    def get(self, request: HttpRequest, *args: Any, response_type: str = "", **kwargs: Any) -> HttpResponse | JsonResponse:
        if not response_type and not request.user.is_authenticated:
            return HttpResponse("", status=401)

        return self._get(request, *args, response_type=response_type, **kwargs)

    @api_key_check
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        return self._post(request, *args, **kwargs)
