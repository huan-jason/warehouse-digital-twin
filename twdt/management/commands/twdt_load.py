import csv
from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction

from twdt import models


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

                models.Warehouse.objects.update_or_create(
                    warehouse_code=warehouse_code,
                    defaults=row,
                )

    def load_rack(self, **options: Any) -> None:

        with open(f"twdt/fixtures/racks.csv") as fp:

            for row in  csv.DictReader(fp):
                warehouse_code: str = row.pop("warehouse_code")
                rack_no: int = int(row.pop("rack_no"))

                models.Warehouse.objects.update_or_create(
                    warehouse__warehouse_code=warehouse_code,
                    rack_no=rack_no,
                    defaults=row,
                )

    def load_rack_location(self, **options: Any) -> None:

        with open(f"twdt/fixtures/rack_locations.csv") as fp:

            for row in  csv.DictReader(fp):
                warehouse_code: str = row.pop("warehouse_code")
                rack_no: int = int(row.pop("rack_no"))
                location_id: str = row.pop("location_id")

                models.Warehouse.objects.update_or_create(
                    rack__warehouse__warehouse_code=warehouse_code,
                    rack__rack_no=rack_no,
                    location_id=location_id,
                    defaults=row,
                )

    def load_pallet(self, **options: Any) -> None:

        with open(f"twdt/fixtures/pallets.csv") as fp:

            for row in  csv.DictReader(fp):
                warehouse_code: str = row.pop("warehouse_code")
                location_id: str = row.pop("location_id")
                pallet_id: str = row.pop("pallet_id")

                models.Warehouse.objects.update_or_create(
                    rack_location__rack__warehouse__warehouse_code=warehouse_code,
                    rack_location__location_id=location_id,
                    pallet_id=pallet_id,
                    defaults=row,
                )
