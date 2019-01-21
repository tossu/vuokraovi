from peewee import *
import multiprocessing
from search import city_apartment_ids
from apartment import get_apartment

db = SqliteDatabase('apartments.db')

class Apartment(Model):
    number = IntegerField(null=True)
    city = CharField(null=True)
    district = CharField(null=True)
    building_type = CharField(null=True)
    description = CharField(null=True)
    short_description = CharField(null=True)
    room_count = CharField(null=True)
    squares = FloatField(null=True)
    condition = CharField(null=True)
    rent = FloatField(null=True)
    pets = BooleanField(null=True)
    smoking = BooleanField(null=True)
    floor = IntegerField(null=True)
    max_floor = IntegerField(null=True)
    estate = CharField(null=True)
    build_year = IntegerField(null=True)
    energy_effiency = CharField(null=True)
    dorm = BooleanField(null=True)
    
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
