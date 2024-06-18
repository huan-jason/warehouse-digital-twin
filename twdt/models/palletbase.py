from django.db.models import (
    CharField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    Model,
    PROTECT,
    TextField,
)


class PalletBase(Model):
    rack_location = ForeignKey("twdt.RackLocation", on_delete=PROTECT)
    owner = CharField(max_length=256, db_index=True)
    product_code = CharField(max_length=64, db_index=True)
    description = TextField()
    expiry_date = DateTimeField()
    quantity_on_hand = IntegerField()
    age = IntegerField()
    balance_shelve_life_to_expire = IntegerField()
    product_group = CharField(max_length=64, db_index=True)
    created = DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True

    def balance_shelf_life_percentage(self) -> float:
        return (
            0 if not self.age else
            round(self.balance_shelve_life_to_expire * 100 / self.age)
        )
