from datetime import timedelta
import json
from typing import Any, cast

from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone

from twdt.models import Device, DeviceLocation
from .baseview import BaseView


class DeviceLocationView(BaseView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse("", status=405)

    def _post(self,
        request: HttpRequest,
        name: str | None = None,
        days: int | None = None,
    ) -> JsonResponse:

        if not name:
            return self.new_location(request)

        if days:
            return self.history(request=request, name=name, days=days)

        device_qs: QuerySet[Device] = Device.objects.filter(name=name)
        device_obj: Device = device_qs.get()

        device_dict: dict[str, Any] = cast(Any, device_qs.values().first())
        device_dict["coordinates"] = device_obj.coordinates

        return JsonResponse({
            "data_type": "device",
            "data": device_dict,
        })

    def history(self, request: HttpRequest, name: str, days: int) -> JsonResponse:

        device_location_qs: QuerySet[DeviceLocation, Any] = cast(Any, DeviceLocation.objects
            .filter(
                device__name=name,
                created__gte=timezone.now().date() - timedelta(days=days),
            )
            .order_by("-created")
            .values()
        )
        return JsonResponse({
            "data_type": "device_history",
            "data": list(device_location_qs),
        })

    def new_location(self, request: HttpRequest) -> JsonResponse:
        data: dict[str, Any] = json.loads(request.body)
        if not { "name", "position" } <= set(data.keys()):
            return JsonResponse({}, status=400)

        try:
            coordinates: dict[str, Any] = data["position"]
        except Exception:
            return JsonResponse({}, status=400)

        return JsonResponse({
            "data": model_to_dict(
                DeviceLocation.new(
                    name=data["name"],
                    coordinates=coordinates,
                )
            ),
        })
