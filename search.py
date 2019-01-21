import requests
from bs4 import BeautifulSoup
import multiprocessing

def search_page_url(city, page=None):
    url = "https://www.vuokraovi.com/vuokra-asunnot/" + str(city)
    if page:
        return url + "/?page=" + str(page)
    return url

def search_page_apartment_ids(url):
    """ Scrapes apartment IDs from search page """

    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    link_elements = [row.find('a', attrs={'class': 'list-item-link'},  href=True) for row in soup.body.find_all('div', attrs={'class': 'row top-row'})]
    return list(map(lambda a: a['href'].split('?')[0].split('/')[-1], link_elements))
    
def city_apartment_ids(city):
    """ We scrape every search page for apartment page IDs """

    search_page_html = requests.get(search_page_url(city))
    search_page_soup= BeautifulSoup(search_page_html.text, "html.parser")
    pagination_element = search_page_soup.body.find('ul', attrs={'class', 'pagination'}).find_all('li')
    last_page_number = int(pagination_element[-2].text.strip())
    search_pages_range = range(1, last_page_number+1)

    search_page_urls = list(map(lambda page: search_page_url(city, page), search_pages_range))
    
    pool = multiprocessing.Pool()
    apartment_ids = sum(pool.map(search_page_apartment_ids, search_page_urls), []) # sum flattens list
   
    return apartment_ids

if __name__ == "__main__":
    print(city_apartment_ids("Jyväskylä"))
