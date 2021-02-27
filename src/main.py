import multiprocessing
from search import city_apartment_ids
from apartment import get_apartment
from database import Apartment, db

if __name__ == "__main__":
    apartment_ids = city_apartment_ids("Jyväskylä")

    db.connect()
    db.create_tables([Apartment])

    pool = multiprocessing.Pool(processes=4)
    apartments = pool.map(get_apartment, apartment_ids)

    for a in apartments:
        if not a:
            continue
        Apartment.create(**a)
