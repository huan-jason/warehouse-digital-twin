from uuid import uuid4, UUID

from django.db.models import (
    CharField,
    DateTimeField,
    JSONField,
    Model,
    TextField,
)


def new_api_key(result: str = "str") -> str | UUID:
    uuid: UUID = uuid4()
    return (
        str(uuid) if result == "str"
        else uuid.hex if result == "hex"
        else uuid
    )


class ApiKey(Model):
    api_key = CharField(max_length=64, unique=True, default=new_api_key, blank=True)
    expiry = DateTimeField()
    remarks = TextField()
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    ip_addresses = JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return self.api_key

    @classmethod
    def new_api_key(self, result: str = "str") -> str | UUID:
        return new_api_key(result)
