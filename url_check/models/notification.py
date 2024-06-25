from django.db.models import (
    EmailField,
    ForeignKey,
    Model,
    PROTECT,
    TextField,
)


class Notification(Model):
    notification_group = ForeignKey("url_check.NotificationGroup", on_delete=PROTECT)
    email = EmailField()
    remarks = TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.notification_group} :: {self.email}"
