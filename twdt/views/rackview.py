from typing import Any, Optional, cast

from django.db.models import QuerySet, F
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from twdt.models import Rack, RackLocation


class RackView(View):

    def get(self,
        request: HttpRequest,
        warehouse_code: str,
        rack_no: Optional[int] = None,
        response_type: str = "",
    ) -> HttpResponse | JsonResponse:

        if not response_type and not request.user.is_authenticated:
            return HttpResponse("", status=401)

        if not rack_no:
            return self.rack_list(request=request, warehouse_code=warehouse_code, response_type=response_type)

        qs: QuerySet[Rack] = (Rack.objects
            .filter(
                warehouse__warehouse_code=warehouse_code,
                rack_no=rack_no,
            )
            .annotate(warehouse_code=F("warehouse__warehouse_code"))
        )
        rack: dict[str, Any] = cast(Any, qs.values().first())
        rack["rack_locations"] = self.get_rack_locations(qs.first())

        if response_type == "json":
            return JsonResponse({
                "data_type": "rack",
                "data": rack,
            })

        return render(request, "twdt/rack_detail.html", locals())

    def get_rack_locations(self, rack: Optional[Rack]) -> list[dict[str, Any]]:
        if not rack: return []

        qs: QuerySet[RackLocation] = rack.racklocation_set.order_by("location_id")
        rack_locations: list[dict[str, Any]] = list(cast(Any, qs.values()))

        for rack_location, obj in zip(rack_locations, qs):
            rack_location["pallets"] = list(obj.pallet_set.order_by("pallet_id").values())

        return rack_locations

    def post(self,
        request: HttpRequest,
        warehouse_code: str,
        rack_no: Optional[int] = None,
    ) -> JsonResponse:

        return cast(
            JsonResponse,
            self.get(
                request=request,
                rack_no=rack_no,
                warehouse_code=warehouse_code,
                response_type="json",
            ),
        )

    def rack_list(self, request: HttpRequest, warehouse_code: str, response_type: str) -> HttpResponse:

        racks: QuerySet[Rack] = (Rack.objects
            .filter(warehouse__warehouse_code=warehouse_code)
            .order_by("rack_no")
        )

        if response_type == "json":
            return JsonResponse({
                "data_type": "rack_list",
                "data": list(racks.values()),
            })

        return render(request, "twdt/rack_list.html", locals())
