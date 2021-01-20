import bs4
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict
import requests
import json
import os

class AssurlandScraping:
    
    def __init__(self, nb_pages: int) -> None:
        """Scrap articles from Assurland. Set a number of keywords as well
        as the number of pages to look for.
        Args:
            - keywords: a list of tuples (keyword, nb_pages).
        """
        self.nb_pages = nb_pages
        self.scraped_url = self.init_links_memory()
        
        
    def scrap(self) -> Dict:
        """Scrap content from of links retrieved from keywords search.
        """
        content = []
        links = self.get_all_links(self.nb_pages)
        for link in links :
            soup = bs4.BeautifulSoup(requests.get(link).text, 'html.parser')
            content.extend(self.scrap_page(soup))
        return content
    
    
    def get_all_links(self, nb_pages: int) -> List[str]:
        """Iterate through number of pages defined by `keyword`, 
        and retrieve links of articles to scrap.
        """
        all_links = []
        for i in range(1, nb_pages + 1):
            url = f'https://www.assurland.com/presse/revue-de-presse-assurance-page{i}.html'
            try : 
                soup = bs4.BeautifulSoup(requests.get(url).text)
                page_links = self.get_links(soup)
                all_links.extend(self.compare_set_scraped(page_links))
            except:
                break
        with open('links/set_url_risques.json', 'w') as f:
            json.dump(self.scraped_url, f, indent=4)
        f.close()
        return all_links
    
    
    def scrap_page(self, soup: BeautifulSoup) -> List[str]:
        """Scrap specific page and return a list of paragraphs.
        """
        paragraph = soup.find('div', class_='al_text').find_all('p')
        content = []
        for p in paragraph:
            if not p.text == ' ' and not 'https://www.' in p.text:
                content.append(self.clean_par(p.text))
        return content
    
    def compare_set_scraped(self, links: List[str]) -> List[str]:
        """ Verifying that a link retrieved for a keyword was not precedently retrieved by an other keyword
            - links : list of retrieved url to inspect
        """
        intersect = list(set(self.scraped_url).intersection(links))
        links = list(set(links))
        if intersect is not [] :
            for i in intersect : 
                links.remove(i)
        self.scraped_url.extend(links)
        return links
    
    @staticmethod 
    def get_links(soup: BeautifulSoup) -> List[str]:
        """Get all links in a page.
        """
        list_href = []
        sections = soup.find_all('div', class_= 'al_articleItem')
        for section in sections :
            list_href.append('https://assurland.com'+section.find('a').get('href'))  
        return list_href
    
    @staticmethod
    def clean_par(par: str) -> str:
        cleaned_par = par.replace('\xa0', ' ').replace('(...)', '')
        return cleaned_par
    
    @staticmethod
    def init_links_memory() -> List[str]: 
        if not os.path.exists('links'):
            os.mkdir('links')
        if not os.path.exists('links/set_url_assurland.json'):
            with open('links/set_url_assurland.json', 'w') as f:
                scraped_url=[]
                json.dump(scraped_url, f)
            f.close()
        else :
            with open('links/set_url_assurland.json', 'r') as f:
                scraped_url = json.load(f)
            f.close()
        return scraped_url