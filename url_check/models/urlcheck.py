from django.db.models import (
    CharField,
    ForeignKey,
    IntegerField,
    Model,
    PROTECT,
    TextField,
    URLField,
)


class UrlCheck(Model):
    url_group = ForeignKey('url_check.UrlGroup', on_delete=PROTECT)
    name = CharField(max_length=64, db_index=True)
    url = URLField()
    notification_group = ForeignKey("url_check.NotificationGroup", on_delete=PROTECT)
    remarks = TextField(null=True, blank=True)
    timeout = IntegerField(default=10)
    status_code = IntegerField(null=True, blank=True, default=200)
    check_text = TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.url_group} :: {self.name}"
