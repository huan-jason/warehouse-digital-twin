from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from twdt.models import RackLocation


class RackLocationView(View):

    def get(self, request: HttpRequest, location_id: str, response_type: str = "") -> HttpResponse | JsonResponse:
        rack_location: QuerySet[RackLocation] = RackLocation.objects.filter(location_id=location_id)

        if response_type == "json":
            return JsonResponse({
                "data_type": "rack_location",
                "data": rack_location.values().first(),
            })

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
