from django.db.models import CharField
from .palletbase import PalletBase


class PalletHistory(PalletBase):
    pallet_id = CharField(max_length=64, db_index=True)

    class Meta:
        verbose_name_plural = "Pallet history"

    def __str__(self) -> str:
        return f"{self.rack_location}::{self.pallet_id}::{self.created}"
