from typing import Any, Optional, cast

from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from twdt.models import Pallet
from .baseview import BaseView
from .utils import remove_keys


class PalletView(BaseView):

    def _get(self,
        request: HttpRequest,
        pallet_id: str,
        days: Optional[int] = None,
        response_type: str = "",
    ) -> HttpResponse | JsonResponse:

        if days:
            return self.history(request=request, pallet_id=pallet_id, days=days)

        pallet_qs: QuerySet[Pallet] = Pallet.objects.filter(pallet_id=pallet_id)
        pallet_obj: Pallet = pallet_qs.get()
        pallet_dict: dict[str, Any] = cast(Any, pallet_qs.values().first())

        pallet_dict["rack_location"] = model_to_dict(pallet_obj.rack_location)
        pallet_dict["rack"] = model_to_dict(pallet_obj.rack_location.rack)
        pallet_dict["warehouse"] = model_to_dict(pallet_obj.rack_location.rack.warehouse)


        if response_type == "json":
            return JsonResponse({
                "data_type": "pallet",
                "data": pallet_dict,
            })

        warehouse: dict[str, Any] = remove_keys(pallet_dict.pop("warehouse"))
        rack: dict[str, Any] = remove_keys(pallet_dict.pop("rack"))
        rack["occupancy"] = f"{pallet_obj.rack_location.rack.occupancy}%"
        rack_location: dict[str, Any] = remove_keys(pallet_dict.pop("rack_location"))
        pallet: dict[str, Any] = remove_keys(pallet_dict)

        return render(request, "twdt/pallet_detail.html", locals())

    def history(self, request: HttpRequest, pallet_id: str, days: int) -> HttpResponse:
        return HttpResponse('TO DO')

    def _post(self, request: HttpRequest, pallet_id: str) -> JsonResponse:

        return cast(
            JsonResponse,
            self.get(
                request=request,
                pallet_id=pallet_id,
                response_type="json",
            ),
        )

