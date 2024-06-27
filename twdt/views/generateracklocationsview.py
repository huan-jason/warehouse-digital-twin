from io import StringIO
from typing import Any, TextIO, cast

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from twdt.models import Warehouse
from twdt.utils import CSV, generate_location_coordinates, GenerateLocationCoordinatesProps


class GenerateRackLocationsView(View):

    def csv_upload(self, request: HttpRequest) -> HttpResponse:
        data: TextIO = StringIO(request.FILES["csv_file"].read().decode("utf8"))

        reader: CSV = CSV(data, template="static/generate_rack_locations.csv")
        count: int = 0

        for item in reader:
            count += generate_location_coordinates(
                cast(GenerateLocationCoordinatesProps, item)
            )

        messages.success(request, f"Records updated: {count}")
        return redirect("/admin/twdt/racklocation/")


    def get(self, request: HttpRequest) -> HttpResponse:
        warehouses: list[dict[str, str]] = list(cast(Any, Warehouse.objects.values("warehouse_code", "name")))
        return render(request, "twdt/generate_rack_locations.html", locals())

    def post(self, request: HttpRequest) -> HttpResponse:
        if "csv" in request.GET:
            try:
                return self.csv_upload(request)
            except Exception as exc:
                upload_error_message: str = str(exc)
                return render(request, "twdt/generate_rack_locations.html", locals())

        count: int = generate_location_coordinates(cast(GenerateLocationCoordinatesProps, {
            key: request.POST[key]
            for key in request.POST.keys()
        }))
        messages.success(request, f"Records updated: {count}")
        return redirect("/admin/twdt/racklocation/")
