import csv
from datetime import datetime, timezone
from typing import Any, Generator

from django.core.management.base import BaseCommand
from django.db import transaction

from twdt.models import (
    Pallet,
    PalletHistory,
    Rack,
    RackLocation,
    Warehouse,
)


class Command(BaseCommand):

    def get_data(self, filename: str) -> Generator[dict[str, Any], None, None]:

        with open(f"twdt/fixtures/{filename}") as fp:

            for i, row in enumerate(csv.DictReader(fp), 1):
                print(i, end="\r")
                yield row

            print("\n")

    def handle(self, *args: Any, **options: Any) -> None:

        # with transaction.atomic(): self.load_warehouse(**options) zzz
        # with transaction.atomic(): self.load_rack(**options)
        # with transaction.atomic(): self.load_rack_location(**options)
        with transaction.atomic(): self.load_pallet(**options)

    def load_warehouse(self, **options: Any) -> None:
        print("Loading warehouses...")

        for row in self.get_data("warehouses.csv"):
            warehouse_code: str = row.pop("warehouse_code")

            Warehouse.objects.update_or_create(
                warehouse_code=warehouse_code,
                defaults=row,
            )

    def load_rack(self, **options: Any) -> None:
        print("Loading racks...")
        warehouses: dict[str, Warehouse] = {}

        for row in self.get_data("racks.csv"):
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
        print("Loading rack locations...")
        racks: dict[str, Rack] = {}

        for row in self.get_data("pallets.csv"):
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
            )

    def load_pallet(self, **options: Any) -> None:
        print("Loading pallets...")
        rack_locations: dict[str, RackLocation] = {}

        for row in self.get_data("pallets.csv"):
            row.pop("warehouse_code")
            location_id: str = row.pop("location_id")
            pallet_id: str = row.pop("pallet_id")

            rack_location: RackLocation =  rack_locations.setdefault(
                location_id,
                RackLocation.objects.get(location_id=location_id),
            )
            row["expiry_date"] = datetime.strptime(
                row["expiry_date"],
                "%m/%d/%Y",
            ).replace(tzinfo=timezone.utc)

            Pallet.objects.update_or_create(
                rack_location=rack_location,
                pallet_id=pallet_id,
                defaults=row,
            )

            PalletHistory.objects.update_or_create(
                rack_location=rack_location,
                pallet_id=pallet_id,
                defaults=row,
            )

