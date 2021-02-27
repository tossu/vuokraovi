import requests
from bs4 import BeautifulSoup
import multiprocessing
from functools import reduce

ROOM_COUNT = {
    "Yksiö": 1,
    "Kaksio": 2,
    "3 huonetta": 3,
    "4 huonetta": 4,
    "5 +": 5
}

SAUNA_OWN = 1
SAUNA_CONDOMINIUM = 2
SAUNA_BOTH = 3

def parse_location(row):
    try:
        elements = row.find('td').find_all('a')
        elements.append(row.find('td').find('span'))
        location = list(map(lambda x: x.text, elements))
        return {"city": location[0].strip().lower(),
                "zone": location[1].strip().lower(),
                "street": location[2].strip().lower()}
    except Exception:
        print("error in parse_location, with value: " + row)
        return {}

def parse_rent(content):
    # TODO: Make tests
    try:
        content = content.replace(",", ".")
        numbers = [s for s in list(content) if s.isdigit() or s == "."]
        return float("".join(numbers))
    except Exception:
        print("error in parse_rent, with value: " + content + " numbers: " + str(numbers))
        return None

def parse_row(panel_header, row):
    header = row.find('th').text.strip().replace(":", "").lower()

    if not header in ["asumismuoto", "kohdenumero", "vuokra", "asuinpinta-ala", "huoneiden lukumäärä", "tilat ja varustelu", "sijainti"]:
        return {}

    content = row.find('td').get_text(strip=True)

    if header == "asumismuoto" and content != "vapaarahoitteinen":
        raise Exception("Asumismuoto ei ole vapaarahoitteinen!")

    if header == "kohdenumero":
        return {"id": int(content)}

    if header == "vuokra":
        if not "€/kk" in content:
            raise Exception("Vuokra ei ole kuukausi maksullinen!")
        return {"rent": parse_rent(content)}

    if header == "asuinpinta-ala":
        try:
            return {"squares": float(content.split(" ")[0].replace(",", "."))}
        except Exception:
            print("error in asuinpinta-ala, with value: " + content)
            return {}

    if header == "huoneiden lukumäärä":
        return {"rooms": ROOM_COUNT[content]}

    if panel_header == "perustiedot" and header == "tilat ja varustelu":
        data = {}
        if "oma sauna" in content:
            data["sauna"] = SAUNA_OWN
        if "taloyhtiössä sauna" in content:
            data["sauna"] = SAUNA_CONDOMINIUM
        if "oma sauna" in content and "taloyhtiössä sauna" in content:
            data["sauna"] = SAUNA_BOTH
        if "parveke" in content:
            data["balcony"] = True
        return data

    if panel_header == "taloyhtiö" and header == "tilat ja varustelu":
        if "elevator" in content:
            return {"elevator": True}

    if header == "sijainti":
        return parse_location(row)

    # Default case
    return {}

def parse_panel(panel):
    panel_header = panel.find('h3', attrs={'class': 'panel-title'})\
            .text.strip().lower()

    # "perustiedot" and "kustannukset" are in every apartment, "taloyhtiö" is not always
    if not panel_header in ["perustiedot", "kustannukset", "taloyhtiö"]:
        return {}

    rows = panel.find_all('tr')
    return reduce(lambda l, row: l.update(parse_row(panel_header, row)) or l, rows, {})


def apartment_data(apartment_id):
    url = "https://www.vuokraovi.com/" + str(apartment_id)

    request = requests.get(url)
    # sometimes apartment is removed and returns 404
    if request.status_code != 200:
        return None # TODO: FIX THIS, throw exception?

    soup = BeautifulSoup(request.text, "html.parser")
    panels = soup.find_all('div', attrs={'class': 'panel panel-default'})

    return reduce(lambda l, panel: l.update(parse_panel(panel)) or l, panels, {})

def get_apartment(apartment_id):
    try:
        return apartment_data(apartment_id)
    except Exception as e:
        print("ERROR AT: " + str(apartment_id))
        print(str(e))
        return {}

if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter(depth=6)
    #pp.pprint(get_apartment(705286))
    #pp.pprint(get_apartment(724334))
    # pp.pprint(get_apartment(803895))
    pp.pprint(get_apartment(610266))    
