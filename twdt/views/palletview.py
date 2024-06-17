from copy import deepcopy
from datetime import timedelta
from typing import Any, Optional, cast

from django.db.models import QuerySet
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone

from twdt.models import Pallet, PalletHistory
from .baseview import BaseView
from .utils import remove_keys


class PalletView(BaseView):

    def _get(self,
        request: HttpRequest,
        pallet_id: str,
        days: Optional[int] = None,
        response_type: str = "",
    ) -> HttpResponse | JsonResponse:

        pallet_qs: QuerySet[Pallet] = Pallet.objects.filter(pallet_id=pallet_id)
        pallet_obj: Pallet = pallet_qs.get()

        pallet_dict: dict[str, Any] = cast(Any, pallet_qs.values().first())

        pallets: list[dict[str, Any]] = (
            self.get_pallet_history(pallet_id, days) if days else
            self.get_pallet(pallet_dict)
        )

        pallet_dict["rack_location"] = model_to_dict(pallet_obj.rack_location)
        pallet_dict["rack"] = model_to_dict(pallet_obj.rack_location.rack)
        pallet_dict["warehouse"] = model_to_dict(pallet_obj.rack_location.rack.warehouse)
        if days:
            pallet_dict["history"] = pallets


        if response_type == "json":
            return JsonResponse({
                "data_type": "pallet",
                "data": pallet_dict,
            })

        warehouse: dict[str, Any] = remove_keys(pallet_dict.pop("warehouse"))
        rack: dict[str, Any] = remove_keys(pallet_dict.pop("rack"))
        rack["occupancy"] = f"{pallet_obj.rack_location.rack.occupancy}%"
        rack_location: dict[str, Any] = remove_keys(pallet_dict.pop("rack_location"))

        hide_link: bool = True
        table_view: bool = bool(days)

        return render(request, "twdt/pallet_detail.html", locals())

    def get_pallet(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        pallet_info: dict[str, Any] = remove_keys(deepcopy(data), ["pallet_id"])
        return [pallet_info]

    def get_pallet_history(self, pallet_id: str, days: int) -> list[dict[str, Any]]:
        return [
            remove_keys(cast(Any, item), ["pallet_id"])
            for item in PalletHistory.objects
            .filter(
                pallet_id=pallet_id,
                created__date__gte=timezone.now().date() - timedelta(days=days)
            )
            .order_by("-created")
            .values()
        ]

    def _post(self,
        request: HttpRequest,
        pallet_id: str,
        days: Optional[int] = None,
    ) -> JsonResponse:

        return cast(
            JsonResponse,
            self.get(
                request=request,
                pallet_id=pallet_id,
                days=days,
                response_type="json",
            ),
        )
