import json
import os
from typing import List, Tuple, Dict

import bs4
import requests
from bs4 import BeautifulSoup


class MarianneScraping:

    def __init__(self, keywords: List[Tuple], memory: bool = False) -> None:
        """Scrap articles from Revue Risques. Set a number of keywords as well
        as the number of pages to look for.
        Args:
            - keywords: a list of tuples (keyword, limit).
            - memory: bool
        """
        self.keywords = keywords
        self.memory = memory
        self.scraped_url = self.init_links_memory()

    def scrap_from_scratch(self) -> Dict:
        output = {}
        for keyword, nb_pages in self.keywords:
            links = self.get_all_links(keyword, nb_pages)
            content = self.scrap_from_links(links)
            output[keyword] = content
        return output

    def scrap_from_links(self, links: List[str]) -> List:
        """Scrap content from of links retrieved from keywords search.
        """
        content = []
        for link in links:
            soup = bs4.BeautifulSoup(requests.get(link).text, 'html.parser')
            content.extend(self.scrap_page(soup))
        return content

    def get_all_links(self, keyword: str, limit: int) -> List[str]:
        """Iterate through number of pages defined by `keyword`, 
        and retrieve links of articles to scrap.
        """
        links = []
        url = f'https://api-content-manager.marianne.net/contents?_page=1&_limit={limit}&q={keyword}&_fields=title%2Csurtitle%2Curl%2CmainMedia%2Cwriters%2Cpublication%2Cpremium%2CisVideoArticle&contentType=article%2Cquizz&_sort=publication.date&_order=desc'

        soup = json.loads(requests.get(url).text)
        page_links = self.get_links(soup)
        links.extend(self.compare_set_scraped(page_links))

        if self.memory:
            with open('links/set_url_marianne.json', 'w') as f:
                json.dump(self.scraped_url, f, indent=4)

        return links

    def compare_set_scraped(self, links: List[str]) -> List[str]:
        """ Verifying that a link retrieved for a keyword was not precedently retrieved by an other keyword
            - links : list of retrieved url to inspect
        """
        intersect = list(set(self.scraped_url).intersection(links))
        links = list(set(links))
        if len(intersect) > 0:
            for i in intersect:
                links.remove(i)
        self.scraped_url.extend(links)
        return links

    def scrap_page(self, soup: BeautifulSoup) -> List[str]:
        """Scrap specific page and return a list of paragraphs.
        """
        par = soup.find_all('p', class_='article-text')
        content = []
        for p in par:
            content.append(self.clean_par(p.text))
        return content

    def init_links_memory(self) -> List[str]:
        scraped_url = []

        if self.memory:

            if not os.path.exists('links'):
                os.mkdir('links')

            if not os.path.exists('links/set_url_marianne.json'):
                with open('links/set_url_marianne.json', 'w') as f:
                    scraped_url = []
                    json.dump(scraped_url, f)
            else:
                with open('links/set_url_marianne.json', 'r') as f:
                    scraped_url = json.load(f)

        return scraped_url

    @staticmethod
    def get_links(json: List[Dict]) -> List[str]:
        """Get all links in a page.
        """
        list_href = []
        for article in json:
            if article['premium'] == False and article['isVideoArticle'] == False:
                list_href.append('https://marianne.net' + article['url'])
        return list_href

    @staticmethod
    def clean_par(par: str) -> str:
        cleaned_par = par.replace('\xa0', ' ').replace('(...)', '').replace('\u2009', ' ')
        return cleaned_par
