Scraperi vuokraovi palveluun.
Hakee tällä hetkellä vain Jyväskylän asunnot, mutta tämä on helposti muutettavissa koodissa.
Scripti tekee "aparments.db" sqlite tietokannan jota on helppo selata.

# Usage
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python vuokraovi.py


# Or use docker
docker build -t vuokraovi .
docker run -it --name=vuokra vuokraovi
docker cp vuokra:/opt/apartments.db .
