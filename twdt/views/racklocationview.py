from typing import Any, cast

from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from twdt.models import RackLocation
from .baseview import BaseView
from .utils import remove_keys


class RackLocationView(BaseView):

    def _get(self, request: HttpRequest, location_id: str, response_type: str = "") -> HttpResponse | JsonResponse:

        rack_location_qs: QuerySet[RackLocation] = RackLocation.objects.filter(location_id=location_id)
        if not rack_location_qs.count():
            return HttpResponse("", status=404)

        rack_location_obj: RackLocation = rack_location_qs.get()
        rack_location: dict[str, Any] = cast(Any, rack_location_qs.values().first())

        rack_location["pallets"] = list(
            rack_location_obj.pallet_set.order_by("pallet_id").values()
        )
        rack_location["rack"] =  model_to_dict(rack_location_obj.rack)
        rack_location["warehouse"] = model_to_dict(rack_location_obj.rack.warehouse)

        if response_type == "json":
            return JsonResponse({
                "data_type": "rack_location",
                "data": rack_location,
            })

        warehouse: dict[str, Any] = remove_keys(rack_location.pop("warehouse"))
        rack: dict[str, Any] = remove_keys(rack_location.pop("rack"))
        rack["occupancy"] = f"{rack_location_obj.rack.occupancy}%"
        pallets: list[dict[str, Any]] = [
            remove_keys(data)
            for data in rack_location.pop("pallets")
        ]
        rack_location = remove_keys(rack_location)

        return render(request, "twdt/rack_location_detail.html", locals())

    def _post(self, request: HttpRequest, location_id: str) -> JsonResponse:

        return cast(
            JsonResponse,
            self.get(
                request=request,
                location_id=location_id,
                response_type="json",
            ),
        )
