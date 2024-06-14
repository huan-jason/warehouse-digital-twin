from typing import Optional, cast

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from twdt.models import Rack


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

        rack: QuerySet[Rack] = Rack.objects.filter(
            warehouse__warehouse_code=warehouse_code,
            rack_no=rack_no,
        )

        if response_type == "json":
            return JsonResponse({
                "data_type": "rack",
                "data": rack.values().first(),
            })

        return render(request, "twdt/rack_detail.html", locals())

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
