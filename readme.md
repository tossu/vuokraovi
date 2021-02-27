Scraperi vuokraovi palveluun.
Hakee tällä hetkellä vain Jyväskylän asunnot, mutta tämä on helposti muutettavissa koodissa.
Scripti tekee "aparments.db" sqlite tietokannan jota on helppo selata.

# Usage
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

# Or use docker
```
docker build -t vuokraovi .
docker run -it --name=vuokra vuokraovi
docker cp vuokra:/opt/apartments.db .
```

# You can use db from bash like this
```
sqlite3 apartments.db "select 'https://www.vuokraovi.com/vuokra-asunto/jyvaskyla/kortepohja/kerrostalo/' || id from apartments where rooms = 2 and rent < 630 and zone='kortepohja'";
```

```
sqlite3 apartments.db "select 'https://www.vuokraovi.com/vuokra-asunto/jyvaskyla/' || zone || '/kerrostalo/' || id from apartments where rooms = 2 and rent < 630 and squares > 50";
```
