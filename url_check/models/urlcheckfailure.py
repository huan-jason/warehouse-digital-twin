from django.db.models import (
    DateField,
    ForeignKey,
    IntegerField,
    Model,
    PROTECT,
    TextField,
)


class UrlCheckFailure(Model):
    url_check = ForeignKey('url_check.UrlCheck', on_delete=PROTECT)
    time = DateField(auto_now=True, db_index=True)
    remarks = TextField()
    status_code = IntegerField()

    def __str__(self) -> str:
        return f"{self.url_check} :: {self.time}"
