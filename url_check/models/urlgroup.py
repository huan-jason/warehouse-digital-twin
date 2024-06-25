from django.db.models import (
    CharField,
    Model,
    TextField,
)


class UrlGroup(Model):
    name = CharField(max_length=64, unique=True)
    remarks = TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
