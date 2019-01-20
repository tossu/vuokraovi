import requests
from bs4 import BeautifulSoup
import multiprocessing
import re

def parse_row_header(info_row):
    return info_row.find('th').text.strip().replace(":", "")

def parse_panel(panel):
    rows = panel.find_all('tr') 
    panel = {}

    for row in rows:
        header = row.find('th').text.strip().replace(":", "").lower()
        content = row.find('td')
        panel[header] = content

    return panel

def to_boolean(s):
    return s == 'sallittu'

def to_number_float(s):
    s = parse_text(s)
    return float(s.split(' ')[0].replace(',', '.'))

def to_number_int(s):
    s = parse_text(s)
    if s.isdigit():
        return int(s)
    return None

def parse_city(s):
    return parse_text(s.find_all('a')[0])

def parse_district(s):
    s = parse_text(s.find_all('a')[1])
    if s == '':
        return None
    return s

def parse_text(s):
    return s.text.strip()

def parse_floors(s):
    try:
        s = parse_text(s)
        p = re.match('^([0-9]{1,2})\/?([0-9]{1,2})?[^0-9]?', s)
        if p.group(2) is None:
            return (int(p.group(1)), None)
        return (int(p.group(1)), int(p.group(2)))
    except Exception as e:
        print("error in parse_floors, with value: " + s)
        print(e)
        return (None, None)

def parse_rent(s):
    try:
        s = parse_text(s)
        p = re.match('^([0-9]{1}.?[0-9]+\,?[0-9]+) €/kk$', s)
        p = re.sub('[^0-9]','', p.group(1)).replace(',', '.')
        return float(p)
    except Exception as e:
        print("error in parse_rent, with value: " + s)
        print(e)
        raise


def parse_target(target_id):
    url = "https://www.vuokraovi.com/vuokra-asunto/jyvaskyla/keljonkangas/kerrostalo/" + str(target_id)

    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    x = soup.body.find('div', attrs={'id': 'accordion'})
    panels = x.find_all('div', attrs={'class': 'panel panel-default'})
   
    try:
        description = panels[0].find('div', attrs={'id': 'itempageDescription'}).text.strip()
    except Exception:
        description = None

    # TODO rename x
    x = {**parse_panel(panels[2]), # Perustiedot (Kerros, Kuvaus, Huoneiden lukumäärä, Rakennusvuosi, Asuinpinta-ala, Yleiskunto, Kohdenumero)
         **parse_panel(panels[3]), # Kustannukset (Vuokra)
         **parse_panel(panels[4]), # Kohteen kuvaus (Lemmikit sallittu, Tupakointi sallittu)
         **parse_panel(panels[5])} # Taloyhtiö (Energialuokka, Tilat ja varustelut (hissi))

    info = {}

    def helper(oname, formatf=parse_text):
        if oname in x and not x[oname] == '':
            return formatf(x[oname])
        return None
        
    info['number'] = target_id
    info['build_year'] = helper('rakennusvuosi', to_number_int)

    info['squares'] = helper('asuinpinta-ala', to_number_float)

    info['pets'] = helper('lemmikit sallittu', to_boolean)
    info['smoking'] = helper('tupakointi sallittu', to_boolean)

    info['city'] = helper('sijainti', parse_city)
    info['district'] = helper('sijainti', parse_district)

    floor, max_floor = (None, None) if 'kerros' not in x else parse_floors(x['kerros'])
    info['floor'] = floor
    info['max_floor'] = max_floor

    info['rent'] = parse_rent(x['vuokra'])

    info['building_type'] = helper('tyyppi')
    info['short_description'] = helper('kuvaus')
    info['room_count'] = helper('huoneiden lukumäärä') 
    info['condition'] = helper('yleiskunto')
    info['estate'] = helper('tilat ja varustelu')
    info['energy_effiency'] = helper('energialuokka')

    info['dorm'] = False if 'kuvaus' not in x else 'solu' in parse_text(x['kuvaus']).lower()
    info['description'] = description
    
    return info

def get_apartment(target_id):
    try:
        return parse_target(target_id)
    except Exception as e:
        print("ERROR AT: " + str(target_id))
        print(str(e))
        return {}

def fetch_site(url):
    request = requests.get(url)
    return BeautifulSoup(request.text, "html.parser")

def parse_target_urls(soup):
    targets = soup.body.find_all('div', attrs={'class' : 'list-item-container'})

    urls = []
    for target in targets:
        target_url = target.find('div', attrs={'class': 'row top-row'}).find('a', href=True)['href']
        urls.append(target_url)

    return urls

def parse_target_id(url):
    return int(url.split('?')[0].split('/')[-1])

def parse_target_ids(site):
    return list(map(parse_target_id, parse_target_urls(site)))

def parse_pagination_last_page(site):
    sites = site.body.find('ul', attrs={'class', 'pagination'}).find_all('li')
    return int(sites[-2].text.strip())

def process_page(url):
    site = fetch_site(url)
    return parse_target_ids(site)

def search_page_url(checksum, searchid, page=None):
    url = "https://www.vuokraovi.com/vuokra-asunnot?checksum=" + str(checksum) + "&searchid=" + str(searchid)
    if page:
        return url + "&page=" + str(page)
    return url
    
def search_targets():
    checksum = 981131
    searchid = 223191
    
    first_site = fetch_site(search_page_url(checksum, searchid))
    ids = parse_target_ids(first_site)

    last_page = parse_pagination_last_page(first_site)
    pages = list(map(lambda page: search_page_url(checksum, searchid, page), range(2, last_page+1)))
    
    pool = multiprocessing.Pool()
    result = sum(pool.map(process_page, pages), []) # sum flattens list
    
    ids.extend(result)
    return ids

def get_apartments():
    targets = search_targets()
    pool = multiprocessing.Pool()

    return pool.map(get_apartment, targets)
