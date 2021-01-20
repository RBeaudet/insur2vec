import json
import os
from typing import List, Tuple, Dict

import bs4
import requests
from bs4 import BeautifulSoup


class RisquesScraping:

    def __init__(self, keywords: List[Tuple], memory: bool = False) -> None:
        """Scrap articles from Revue Risques. Set a number of keywords as well
        as the number of pages to look for.
        Args:
            - keywords: a list of tuples (keyword, nb_pages).
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

    def get_all_links(self, keyword: str, nb_pages: int) -> List[str]:
        """Iterate through number of pages defined by `keyword`, 
        and retrieve links of articles to scrap.
        """
        links = []
        for i in range(1, nb_pages + 1):
            url = f'https://www.revue-risques.fr/page/{i}/?s={keyword}'
            try:
                soup = bs4.BeautifulSoup(requests.get(url).text)
                page_links = self.get_links(soup)
                links.extend(self._compare_set_scraped(page_links))
            except Exception:
                break

        if self.memory:
            with open('links/set_url_risques.json', 'w') as f:
                json.dump(self.scraped_url, f, indent=4)

        return links

    def _compare_set_scraped(self, links: List[str]) -> List[str]:
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
        paragraph = soup.find('div', class_='post-content').find_all('p')
        content = []
        for p in paragraph:
            content.append(self.clean_par(p.text))
        return content

    def init_links_memory(self) -> List[str]:
        scraped_url = []

        if self.memory:

            if not os.path.exists('links'):
                os.mkdir('links')

            if not os.path.exists('links/set_url_risques.json'):
                with open('links/set_url_risques.json', 'w') as f:
                    scraped_url = []
                    json.dump(scraped_url, f)
            else:
                with open('links/set_url_risques.json', 'r') as f:
                    scraped_url = json.load(f)

        return scraped_url

    @staticmethod
    def get_links(soup: BeautifulSoup) -> List[str]:
        """Get all links in a page.
        """
        list_href = []
        sections = soup.find_all('h2', class_='entry-title')
        for section in sections:
            list_href.append(section.find('a').get('href'))
        return list_href

    @staticmethod
    def clean_par(par: str) -> str:
        cleaned_par = par.replace('\xa0', ' ').replace('(...)', '')
        return cleaned_par
