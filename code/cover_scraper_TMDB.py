import time
from itertools import cycle

import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
import dateparser
import pandas as pd
from random import shuffle
from tqdm import tqdm
import urllib.parse


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


def cycle_request(url, proxies, head, verbose=False):
    shuffle(proxies)
    proxy_pool = cycle(proxies)
    print(proxies)
    for _ in range(len(proxies)):
        proxy = next(proxy_pool)
        # print(f"Requesting from {proxy}") if verbose else None
        try:
            print("hello")

            response = requests.get(url, proxies={"http:": proxy, "https:": proxy}, headers=head)
            print("hello")
            print(response.raise_for_status())
            print(response.ok)
            if response.content is None:
                print("Blocked by server trying again in 30 seconds") if verbose else None
                time.sleep(30)
                continue
            return response
        except:
            print(f"Connection error, Skipping {proxy}\n") if verbose else None

headers = {
    'Referer': 'https://www.rottentomatoes.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

proxies = list(get_proxies())
print(proxies)

def get_poster_image_url(title, year, prox, verbose=False):
    print(f"Looking for {title} {year}") if verbose else None
    search_url = f"https://www.themoviedb.org/search?language=en-US&query={urllib.parse.quote(title)}"
    url_root = "https://www.themoviedb.org"
    search_page = cycle_request(search_url, prox, headers)
    # print(len(search_page.content))
    print(search_page)
    search_soup = BeautifulSoup(search_page.content, "html.parser")
    search_results = search_soup.find(class_="results flex")
    # print(search_results)
    parsed_results = search_results.find_all(class_="card v4 tight")
    print(f"{len(parsed_results)} results") if verbose else None
    for movie in parsed_results:
        try:
            movie_title = movie.find("div", class_="title").find("h2").getText()
            print("Title: ", movie_title) if verbose else None
            release_date = movie.find(class_="release_date")
            if release_date:
                release_year = dateparser.parse(release_date.getText()).year
            else:
                continue
            # print(str(movie_title).lower(), release_year)
            if (str(movie_title).lower(), release_year) == (title.lower(), year):
                print(movie_title, release_year, " match") if verbose else None
                poster = movie.find("img", class_="poster")
                if poster:
                    poster_URL = url_root + poster.get("srcset").split(",")[1][1:-3]
                    print(poster_URL) if verbose else None
                    return poster_URL
                else:
                    continue
        except TypeError:
            print("Could not match")
            continue

# movies = pd.read_csv("../data/movies_streaming_platforms_cleaned.csv", index_col=False)
# print(movies.head()[["title", "year"]])

movie_poster_db = pd.read_csv("../data/Movie_posterURL.csv")
movies = movie_poster_db[movie_poster_db["posterURL"].isnull()]

movies_data = []
for idx, title, year, _ in tqdm(movies.to_numpy()):
    print(idx, title, year)
    poster_url = get_poster_image_url(title, year, proxies)
    movie_poster_db["posterURL"][idx] = poster_url

movie_poster_db.to_csv("../data/Movie_posterURL.csv")

# df = pd.DataFrame(data=movies_data, columns=["title", "year", "posterURL"])
# df.to_csv("../data/Movie_posterURL.csv")
