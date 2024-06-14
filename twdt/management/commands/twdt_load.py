import csv
from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction

from twdt.models import (
    Pallet,
    Rack,
    RackLocation,
    Warehouse,
)


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> None:

        with transaction.atomic():
            self.load_warehouse(**options)
            self.load_rack(**options)
            self.load_rack_location(**options)
            self.load_pallet(**options)

    def load_warehouse(self, **options: Any) -> None:

        with open(f"twdt/fixtures/warehouses.csv") as fp:

            for row in  csv.DictReader(fp):
                warehouse_code: str = row.pop("warehouse_code")

                Warehouse.objects.update_or_create(
                    warehouse_code=warehouse_code,
                    defaults=row,
                )

    def load_rack(self, **options: Any) -> None:

        warehouses: dict[str, Warehouse] = {}

        with open(f"twdt/fixtures/racks.csv") as fp:

            for row in  csv.DictReader(fp):
                warehouse_code: str = row.pop("warehouse_code")
                rack_no: int = int(row.pop("rack_no"))

                warehouse: Warehouse = warehouses.setdefault(
                    warehouse_code,
                    Warehouse.objects.get(warehouse_code=warehouse_code),
                )

                Rack.objects.update_or_create(
                    warehouse=warehouse,
                    rack_no=rack_no,
                    defaults=row,
                )

    def load_rack_location(self, **options: Any) -> None:

        with open(f"twdt/fixtures/racks.csv") as fp:

            racks: dict[str, Rack] = {}

            for row in  csv.DictReader(fp):
                warehouse_code: str = row.pop("warehouse_code")
                location_id: str = row.pop("location_id")
                rack_no: int = int(location_id[1:3])

                rack: Rack = racks.setdefault(
                    f"{warehouse_code}::{rack_no}",
                    Rack.objects.get(
                        warehouse__warehouse_code=warehouse_code,
                        rack_no=rack_no,
                    ),
                )

                RackLocation.objects.update_or_create(
                    rack=rack,
                    location_id=location_id,
                    defaults=row,
                )

    def load_pallet(self, **options: Any) -> None:

        with open(f"twdt/fixtures/pallets.csv") as fp:

            rack_locations: dict[str, RackLocation] = {}

            for row in  csv.DictReader(fp):
                location_id: str = row.pop("location_id")
                pallet_id: str = row.pop("pallet_id")

                rack_location: RackLocation =  rack_locations.setdefault(
                    location_id,
                    RackLocation.objects.get(location_id=location_id),
                )

                Pallet.objects.update_or_create(
                    rack_location=rack_location,
                    pallet_id=pallet_id,
                    defaults=row,
                )
