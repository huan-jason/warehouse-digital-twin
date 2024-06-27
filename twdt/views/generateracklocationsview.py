from typing import Any, cast

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from twdt.models import Warehouse
from twdt.utils import generate_location_coordinates, GenerateLocationCoordinatesProps


class GenerateRackLocationsView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        warehouses: list[dict[str, str]] = list(cast(Any, Warehouse.objects.values("warehouse_code", "name")))
        return render(request, "twdt/generate_rack_locations.html", locals())

    def post(self, request: HttpRequest) -> HttpResponse:
        count: int = generate_location_coordinates(cast(GenerateLocationCoordinatesProps, {
            key: request.POST[key]
            for key in request.POST.keys()
        }))
        print(count)
        return redirect("/admin/twdt/racklocation/")
