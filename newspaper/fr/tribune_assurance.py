import bs4
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict
import requests
import os
import json
import time

class TribuneAssuranceScraping:
    
    def __init__(self, keywords: List[Tuple]) -> None:
        """Scrap articles from Tribune Assurance. Set a number of keywords as well
        as the number of pages to look for.
        Args:
            - keywords: a list of tuples (keyword, nb_pages).
        """
        self.keywords = keywords
        self.scraped_url = self.init_links_memory()
        
        
    def scrap(self) -> Dict:
        """Scrap content from of links retrieved from keywords search.
        """
        output = {}
        # iterate through keywords
        for keyword, nb_pages in self.keywords:
            # get all the links related to keyword, and parse articles
            content = []
            links = self.get_all_links(keyword, nb_pages)
            for link in links :
                soup = bs4.BeautifulSoup(requests.get(link).text, 'html.parser')
                content.extend(self.scrap_page(soup))
            output[keyword] = content
        return output
    
    
    def get_all_links(self, keyword: str, nb_pages: int) -> List[str]:
        """Iterate through number of pages defined by `keyword`, 
        and retrieve links of articles to scrap.
        """
        all_links = []
        for i in range(1, nb_pages + 1):
            url = f'https://www.tribune-assurance.fr/recherche/?web_cms_search%5BrawContent%5D={keyword}&web_cms_search%5Bsearch%5D=&page={i}'
            try : 
                soup = bs4.BeautifulSoup(requests.get(url).text)
                page_links = self.get_links(soup)
                all_links.extend(self.compare_set_scraped(page_links))
            except:
                break     
        with open('links/set_url_tribune_assurance.json', 'w') as f:
            json.dump(self.scraped_url, f, indent=4)
        f.close()
        return all_links
    
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
    
    def scrap_page(self, soup: BeautifulSoup) -> List[str]:
        """Scrap specific page and return a list of paragraphs.
        """
        paragraph = soup.find('div', class_='article-content').find_all('p')
        content = []
        for p in paragraph:
            cleaned = self.clean_par(p.text)
            if cleaned != ' ':
                content.append(cleaned)
        return content
    
    @staticmethod 
    def get_links(soup: BeautifulSoup) -> List[str]:
        """Get all links in a page.
        """
        list_href = []
        sections = soup.find_all('div', class_= 'media-body')
        for section in sections :
            if section.find('span', class_='free-access') is not None :
                list_href.append('https://www.tribune-assurance.fr'+section.find('a').get('href'))  
        return list_href
    
    @staticmethod
    def init_links_memory() -> List[str]:
        if not os.path.exists('links'):
            os.mkdir('links')
        if not os.path.exists('links/set_url_tribune_assurance.json'):
            with open('links/set_url_tribune_assurance.json', 'w') as f:
                scraped_url=[]
                json.dump(scraped_url, f)
            f.close()
        else :
            with open('links/set_url_tribune_assurance.json', 'r') as f:
                scraped_url = json.load(f)
            f.close()
        return scraped_url
    
    @staticmethod
    def clean_par(par: str) -> str:
        cleaned_par = par.replace('\xa0', ' ').replace('(...)', '')
        return cleaned_par