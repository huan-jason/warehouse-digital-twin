from typing import Any, cast

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from twdt.models import Pallet


class PalletView(View):

    def get(self, request: HttpRequest, pallet_id: str, response_type: str = "") -> HttpResponse | JsonResponse:
        if not response_type and not request.user.is_authenticated:
            return HttpResponse("", status=401)

        pallet: QuerySet[Pallet] = Pallet.objects.filter(pallet_id=pallet_id)

        if response_type == "json":
            return JsonResponse({
                "data_type": "pallet",
                "data": pallet.values().first(),
            })

        return render(request, "twdt/pallet_detail.html", locals())

    def post(self, request: HttpRequest, pallet_id: str) -> JsonResponse:

        return cast(
            JsonResponse,
            self.get(
                request=request,
                pallet_id=pallet_id,
                response_type="json",
            ),
        )

