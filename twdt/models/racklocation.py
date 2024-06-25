from django.db.models import (
    CharField,
    ForeignKey,
    JSONField,
    Model,
    PROTECT,
    UniqueConstraint,
)


class RackLocation(Model):
    rack = ForeignKey("twdt.Rack", on_delete=PROTECT)
    location_id = CharField(max_length=32, unique=True)
    coordinates = JSONField(null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                name="rack_location__unique",
                fields=[
                    "rack",
                    "location_id",
                ],
            ),
        ]

    def __str__(self) -> str:
        return f"{self.rack} :: {self.location_id}"
