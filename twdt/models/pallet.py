from django.db.models import (
    CharField,
    UniqueConstraint,
)
from .palletbase import PalletBase


class Pallet(PalletBase):
    pallet_id = CharField(max_length=64, unique=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                name="pallet__unique",
                fields=[
                    "rack_location",
                    "pallet_id",
                ],
            ),
        ]

    def __str__(self) -> str:
        return f"{self.rack_location}::{self.pallet_id}"
