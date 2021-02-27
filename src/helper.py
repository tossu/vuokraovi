import requests
from bs4 import BeautifulSoup
import multiprocessing
from search import city_apartment_ids


def panel_headers(target_id):
    url = "https://www.vuokraovi.com/vuokra-asunto/jyvaskyla/keljonkangas/kerrostalo/" + str(target_id)

    request = requests.get(url)

    if request.status_code != 200:
        return {'error': 'status code not 200'}

    soup = BeautifulSoup(request.text, "html.parser")
    panels = soup.find_all('div', attrs={'class': 'panel panel-default'})

    headers = list(map(lambda x: x.find('h3', attrs={'class': 'panel-title'})\
            .text.strip().lower(), panels))
    return list(filter(lambda x: x != "sijainti kartalla" and x != "taloyhtiö", headers))

def get_apartment_headers(apartment_id):
    try:
        return panel_headers(apartment_id)
    except Exception as e:
        print("ERROR AT: " + str(apartment_id))
        print(str(e))
        return []

def get_all_headers():
    ids = city_apartment_ids("Jyväskylä")
    headers = {}
    for i in ids:
        headers[i] = get_apartment_headers(i)
    return headers

if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter(depth=6)
    #pp.pprint(get_apartment_headers(803895))
    pp.pprint(get_apartment_headers(798745))

    #pp.pprint(get_all_headers())
