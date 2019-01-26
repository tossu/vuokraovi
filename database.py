from peewee import *
import multiprocessing
from search import city_apartment_ids
from apartment import get_apartment

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

if __name__ == "__main__":
    apartment_ids = city_apartment_ids("Jyväskylä")

    db.connect()
    db.create_tables([Apartment])

    pool = multiprocessing.Pool()
    apartments = pool.map(get_apartment, apartment_ids)

    for a in apartments:
        if not a:
            continue
        Apartment.create(**a)
