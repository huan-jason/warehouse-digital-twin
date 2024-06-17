from django.shortcuts import redirect
from django.urls import path

from . import views


urlpatterns = [
    path("warehouse/<warehouse_code>/", views.WarehouseView.as_view(), name="warehouse_view"),
    path("warehouse/", views.WarehouseView.as_view(), name="warehouse_view"),

    path("rack/<warehouse_code>/<int:rack_no>/", views.RackView.as_view(), name="rack_view"),
    path("rack/<warehouse_code>/", views.RackView.as_view(), name="rack_view"),

    path("rack-location/<location_id>/", views.RackLocationView.as_view(), name="rack_location_view"),

    path("pallet/<pallet_id>/<int:days>/", views.PalletView.as_view(), name="pallet_history_view"),
    path("pallet/<pallet_id>/", views.PalletView.as_view(), name="pallet_view"),

    path("", lambda request: redirect("warehouse_view"), name="index_view"),
]
