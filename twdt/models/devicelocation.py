from typing import Any
from django.db.models import (
    DateField,
    ForeignKey,
    JSONField,
    Model,
    PROTECT,
)


class DeviceLocation(Model):
    device = ForeignKey('twdt.device', on_delete=PROTECT)
    coordinates = JSONField()
    created = DateField(auto_now_add=True)

    class Meta:
        ordering = [
            "device",
            "-created",
        ]

    def __str__(self) -> str:
        return f"{self.device}::{self.created}"

    @classmethod
    def new(cls, name: str, coordinates: dict[str, Any]) -> 'DeviceLocation':
        from .device import Device

        if not { "x", "y", "z" } <= set(coordinates.keys()):
            raise ValueError(f"Invalid coordinates: {coordinates}")

        try: device: Device = Device.objects.get(name=name)
        except Device.DoesNotExist:
            raise ValueError(f"Invalid device name: {name}")

        return cls.objects.create(
            device=device,
            coordinates=coordinates,
        )
