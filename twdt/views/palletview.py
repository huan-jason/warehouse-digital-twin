from typing import Any, Optional, cast

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from twdt.models import Pallet


class PalletView(View):

    def get(self,
        request: HttpRequest,
        pallet_id: str,
        days: Optional[int] = None,
        response_type: str = "",
    ) -> HttpResponse | JsonResponse:

        if days:
            return self.history(request=request, pallet_id=pallet_id, days=days)

        if not response_type and not request.user.is_authenticated:
            return HttpResponse("", status=401)

        pallet: QuerySet[Pallet] = Pallet.objects.filter(pallet_id=pallet_id)

        if response_type == "json":
            return JsonResponse({
                "data_type": "pallet",
                "data": pallet.values().first(),
            })

        return render(request, "twdt/pallet_detail.html", locals())

    def history(self, request: HttpRequest, pallet_id: str, days: int) -> HttpResponse:
        return HttpResponse('TO DO')

    def post(self, request: HttpRequest, pallet_id: str) -> JsonResponse:

        return cast(
            JsonResponse,
            self.get(
                request=request,
                pallet_id=pallet_id,
                response_type="json",
            ),
        )

