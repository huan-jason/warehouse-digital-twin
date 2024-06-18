from typing import Optional
from django.db.models import (
    CharField,
    DateField,
    Model,
    TextField,
)
from twdt.types import Coordinates


class Device(Model):
    name = CharField(max_length=64, unique=True)
    description = TextField(null=True, blank=True, default= "")
    created = DateField(auto_now_add=True)
    updated = DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    @property
    def coordinates(self) -> Coordinates | None:
        from .devicelocation import DeviceLocation

        obj: Optional[DeviceLocation] = self.devicelocation_set.order_by("-created").first()
        return obj.coordinates if obj else None
