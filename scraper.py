import pip._vendor.requests as requests
from bs4 import BeautifulSoup
from urllib.parse import quote
#scraper pobiera dane ze strony rottentomatos.com, 
#strona serialu wyglada inaczej niz strona filmu, dlatego musielismy zaimplementowac 2 rozne tryby funkcji
def GetMovies(movieName):
    urlBase = "https://www.rottentomatoes.com/search?search="
    encodedMovieName = ""
    movies_dict = {}
    if "$" in movieName:
        #spacje zamieniamy na %20%
        encodedMovieName = quote(movieName.replace("$",""),safe='/:?=&')
        page = requests.get(urlBase+encodedMovieName)
        soup = BeautifulSoup(page.content, 'html.parser')
        movie_link = soup.select('search-page-result[slot="tv"]')[0].find_all('a')[0].get('href')
        moviePage = requests.get(movie_link)
        soup = BeautifulSoup(moviePage.content, 'html.parser')
        movie_info = soup.select('section[id="detail_panel"]')[0].select('div[class="panel-body content_body"]')[0].find_all('tr')
        for info in movie_info:
            infoName = info.find_all('td')[0].get_text().replace("\n", " ").strip()
            infoValue = info.find_all('td')[1].get_text().replace("\n", " ").strip()
            movies_dict[infoName] = " ".join(infoValue.split())
        return movies_dict
    
    else:
        encodedMovieName = quote(movieName,safe='/:?=&')   
        page = requests.get(urlBase+encodedMovieName)
        soup = BeautifulSoup(page.content, 'html.parser')
        movie_link = soup.find_all('search-page-media-row')[0].find_all('a')[0].get('href')
        moviePage = requests.get(movie_link)
        soup = BeautifulSoup(moviePage.content, 'html.parser')
        movie_info = soup.find_all('li', class_='meta-row clearfix')[0]
        for info in soup.find_all('li', class_='meta-row clearfix'):
            infoName = info.find_all('div',  class_='meta-label subtle')[0].get_text().replace("\n", " ").strip()  
            infoValue = info.find_all('div',  class_='meta-value')[0].get_text().replace("\n", " ").strip()
            movies_dict[infoName] = " ".join(infoValue.split())
    #zwracamy slownik z informacjiami o filmie/serialu gdzie kluczem jest nazwa informacji
    return movies_dict

    


