from django.db.models import (
    EmailField,
    ForeignKey,
    Model,
    PROTECT,
    TextField,
)


class UrlCheckNotification(Model):
    url_check = ForeignKey("url_check.UrlCheck", on_delete=PROTECT)
    email = EmailField()
    remarks = TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.url_check} :: {self.email}"
