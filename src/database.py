from peewee import *

db = SqliteDatabase('apartments.db')

class Apartment(Model):
    id = UUIDField(primary_key=True)
    city = CharField(null=True)
    zone = CharField(null=True)
    street = CharField(null=True)
    rooms = IntegerField(null=True)
    squares = FloatField(null=True)
    sauna = IntegerField(null=True)
    balcony = BooleanField(null=True)
    rent = FloatField(null=True)

    class Meta:
        database = db
        table_name = 'apartments'
