from typing import Any, Optional, cast

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from twdt.models import Warehouse


class WarehouseView(View):

    def get(self,
        request: HttpRequest,
        warehouse_code: Optional[str] = None,
        response_type: str = "",
    ) -> HttpResponse | JsonResponse:

        if not warehouse_code:
            return self.warehouse_list(request, response_type)

        warehouse: QuerySet[Warehouse] = Warehouse.objects.filter(
            warehouse_code=warehouse_code
        )

        if response_type == "json":
            return JsonResponse({
                "data_type": "warehouse",
                "data": warehouse.values().first(),
            })

        return render(request, "twdt/warehouse_detail.html", locals())

    def post(self, request: HttpRequest, warehouse_code: Optional[str] = None) -> JsonResponse:
        return cast(
            JsonResponse,
            self.get(request=request, warehouse_code=warehouse_code, response_type="json"),
        )

    def warehouse_list(self, request: HttpRequest, response_type: str) -> HttpResponse:

        warehouses: QuerySet[Warehouse, Any] = Warehouse.objects.values().order_by("warehouse_code")

        if response_type == "json":
            return JsonResponse({
                "data_type": "warehouse_list",
                "data": list(warehouses),
            })

        return render(request, "twdt/warehouse_list.html", locals())
