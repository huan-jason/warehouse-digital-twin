import json
from typing import Any
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse

from twdt.models import DeviceLocation
from .baseview import BaseView


class DeviceLocationView(BaseView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse("", status=404)

    def _post(self, request: HttpRequest) -> JsonResponse:
        if not { "name", "position" } <= set(request.POST.keys()):
            return JsonResponse({}, status=400)

        try:
            coordinates: dict[str, Any] = json.loads(request.POST["position"])
        except Exception:
            return JsonResponse({}, status=400)

        return JsonResponse({
            "data": model_to_dict(
                DeviceLocation.new(
                    name=request.POST["name"],
                    coordinates=coordinates,
                )
            ),
        })
