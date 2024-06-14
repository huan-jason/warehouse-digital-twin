from django.db.models import (
    ForeignKey,
    IntegerField,
    Model,
    PROTECT,
    UniqueConstraint,
)


class Rack(Model):
    warehouse = ForeignKey("twdt.Warehouse", on_delete=PROTECT)
    rack_no = IntegerField()
    depth = IntegerField(db_index=True)
    pallet_positions = IntegerField(db_index=True)
    filled_pallet_positions = IntegerField(db_index=True, blank=True, default=0)

    class Meta:
        constraints = [
            UniqueConstraint(
                name="rack__unique",
                fields=[
                    "warehouse",
                    "rack_no",
                ],
            ),
        ]

    def __str__(self) -> str:
        return f"{self.warehouse}::{self.rack_no}"

    def occupancy(self) -> float:
        return self.filled_pallet_positions * 100 / self.pallet_positions
