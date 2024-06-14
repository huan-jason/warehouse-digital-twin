from typing import Any, cast

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from twdt.models import Rack, RackLocation, Warehouse


class RackLocationView(View):

    def get(self, request: HttpRequest, location_id: str, response_type: str = "") -> HttpResponse | JsonResponse:
        if not response_type and not request.user.is_authenticated:
            return HttpResponse("", status=401)

        rack_location_qs: QuerySet[RackLocation] = RackLocation.objects.filter(location_id=location_id)
        if not rack_location_qs.count():
            return HttpResponse("", status=404)

        rack_location_obj: RackLocation = rack_location_qs.get()
        rack_location: dict[str, Any] = cast(Any, rack_location_qs.values().first())

        rack_location["pallets"] = list(
            rack_location_obj.pallet_set.order_by("pallet_id").values()
        )
        rack_location["rack"] = Rack.objects.filter(id=rack_location["rack_id"]).values().first()
        rack_location["warehouse"] = Warehouse.objects.filter(id=rack_location["rack"]["warehouse_id"]).values().first()

        if response_type == "json":
            return JsonResponse({
                "data_type": "rack_location",
                "data": rack_location,
            })

        warehouse: dict[str, Any] = self.remove_keys(rack_location.pop("warehouse"))
        rack: dict[str, Any] = self.remove_keys(rack_location.pop("rack"))
        pallets: list[dict[str, Any]] = [
            self.remove_keys(data)
            for data in rack_location.pop("pallets")
        ]
        rack_location = self.remove_keys(rack_location)


        import json
        from django.core.serializers.json import DjangoJSONEncoder # zzz
        data = json.dumps(
            dict(rack_location=rack_location, warehouse=warehouse, rack=rack, pallets=pallets),
            indent=4, cls=DjangoJSONEncoder
        )

        return render(request, "twdt/rack_location_detail.html", locals())

    def post(self, request: HttpRequest, location_id: str) -> JsonResponse:

        return cast(
            JsonResponse,
            self.get(
                request=request,
                location_id=location_id,
                response_type="json",
            ),
        )

    def remove_keys(self, data: dict[str, Any]) -> dict[str, Any]:
        include_keys: set[str] = {
            "location_id",
            "pallet_id",
        }

        return {
            key.replace("_", " "): val
            for key, val in data.items()
            if not key.endswith("id") or key in include_keys
        }
