import json
import os
from typing import List, Tuple, Dict

import bs4
import selenium.webdriver as webdriver
from bs4 import BeautifulSoup


class UniversiteAssuranceScraping:

    def __init__(self, keywords: List[Tuple], memory: bool = False) -> None:
        """Scrap articles from Revue Risques. Set a number of keywords as well
        as the number of pages to look for.
        Args:
            - keywords: a list of tuples (keyword, nb_pages).
            - memory: bool
        """
        self.keywords = keywords
        self.memory = memory
        options = webdriver.chrome.options.Options()
        self.driver = webdriver.Chrome(options=options)
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
            self.driver.get(link)
            soup = bs4.BeautifulSoup(self.driver.page_source, 'html.parser')
            content.extend(self.scrap_page(soup))
        return content

    def get_all_links(self, keyword: str, nb_pages: int) -> List[str]:
        """Iterate through number of pages
        and retrieve links of articles to scrap.
        """
        links = []

        for i in range(1, nb_pages + 1):
            url = f'https://www.universite-assurance.org/page/{i}/?s={keyword}'
            try:
                self.driver.get(url)
                soup = bs4.BeautifulSoup(self.driver.page_source, 'html.parser')
                page_links = self.get_links(soup)
                links.extend(self.compare_set_scraped(page_links))
            except Exception:
                break

        if self.memory:
            with open('links/set_url_universite_assurance.json', 'w') as f:
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
        par = soup.find('div', class_='entry-content').find_all('p')
        content = []
        for p in par:
            cleaned = self.clean_par(p.text)
            if cleaned != '' and cleaned != ' ':
                content.append(cleaned)
        return content

    def init_links_memory(self) -> List[str]:
        scraped_url = []

        if self.memory:

            if not os.path.exists('links'):
                os.mkdir('links')

            if not os.path.exists('links/set_url_universite_assurance.json'):
                with open('links/set_url_universite_assurance.json', 'w') as f:
                    scraped_url = []
                    json.dump(scraped_url, f)
            else:
                with open('links/set_url_universite_assurance.json', 'r') as f:
                    scraped_url = json.load(f)

        return scraped_url

    @staticmethod
    def get_links(soup: BeautifulSoup) -> List[str]:
        """Get all links in a page.
        """
        list_href = []
        sections = soup.find_all('a', class_='entry-featured-image-url')
        for section in sections:
            list_href.append(section.get('href'))
        return list_href

    @staticmethod
    def clean_par(par: str) -> str:
        cleaned_par = par.replace('\xa0', ' ').replace('(...)', '')
        return cleaned_par
