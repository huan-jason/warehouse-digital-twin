from django.db.models import (
    CharField,
    Model,
    TextField,
)


class Warehouse(Model):
    warehouse_code = CharField(max_length=32, unique=True)
    name = CharField(max_length=64, db_index=True)
    address = TextField(blank=True, null=True, default="")
    remarks = TextField(blank=True, null=True, default="")

    def __str__(self) -> str:
        return self.warehouse_code
