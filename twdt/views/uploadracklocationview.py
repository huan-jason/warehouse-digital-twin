import csv
from io import StringIO
from typing import Any, cast

from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.core.files.uploadedfile import InMemoryUploadedFile

from twdt.models import RackLocation, Rack, Warehouse
from .baseview import BaseView
from .utils import remove_keys


class UploadRackLocationView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "twdt/upload_rack_location.html", locals())

    def check_headers(self, data: list[dict[str, Any]]) -> str | None:
        headers: set[str] = set([item for item in data[0].keys()])
        required_headers: set[str] = {"warehouse", "rack_no", "location_id", "x", "y", "z"}
        missing_headers: set[str] = required_headers - headers
        if not missing_headers:
            return None
        return "Missing headers in CSV file: %s" % ", ".join(sorted(missing_headers))

    def post(self, request: HttpRequest) -> HttpResponse:

        reader: csv.DictReader = csv.DictReader(StringIO(
            cast(Any, request.FILES["csv_file"]).read().decode("utf8")
        ))
        data: list[dict[str, Any]] = [
            {k.strip().lower(): v for k, v in row.items()}
            for row in reader
        ]

        error_message: str | None = self.check_headers(data)
        if error_message:
            return render(request, "twdt/upload_rack_location.html", locals())

        with transaction.atomic():
            try: self.update_rack_locations(data)
            except Exception as exc:
                error_message = str(exc)
                return render(request, "twdt/upload_rack_location.html", locals())

        return redirect("/admin/twdt/racklocation/")

    def update_rack_locations(self, data: list[dict[str, Any]]) -> None:
        for item in data:
            warehouse: Warehouse | None = Warehouse.objects.filter(warehouse_code=item["warehouse"]).first()
            if not warehouse:
                raise Exception(f"Invalid warehouse: {item['warehouse']}")

            rack: Rack | None = Rack.objects.filter(warehouse=warehouse, rack_no=int(item["rack_no"])).first()
            if not rack:
                raise Exception(f"Invalid rack no: {item['rack_no']}")

            RackLocation.objects.update_or_create(
                location_id=item["location_id"],
                defaults={
                    "rack": rack,
                    "coordinates": {
                        "x": float(item["x"]),
                        "y": float(item["y"]),
                        "z": float(item["z"]),
                    },
                },
            )
