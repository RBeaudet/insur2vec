import bs4
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict
import requests
import json
import os
import PyPDF2
import os
import re
import string



class FfaScraping:
    
    def __init__(self, keywords) -> None:
        """Scrap articles from Atlas Magazine. Set a number of keywords as well
        as the number of pages to look for.
        Args:
            - keywords: a list of tuples (keyword, nb_pages).
            - scraped_url stocks previous scraped url for all keywords to avoid inter-keyword repetitions
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
                if soup.find('div', class_='_df_button download') is not None :
                    content.extend(self.scrap_pdf(soup))
                else :
                    content.extend(self.scrap_page(soup))
            output[keyword] = content
        return output
        
    def get_all_links(self, keyword: str, nb_pages: int) -> List[str]:
        """Iterate through number of pages defined by `keyword`, 
        and retrieve links of articles to scrap.
        """
        all_links = []
        for i in range(0, nb_pages + 1):
            url = f'https://www.ffa-assurance.fr/search?search_api_views_fulltext={keyword}&type=2&page={i}'
            try : 
                soup = bs4.BeautifulSoup(requests.get(url).text)
                page_links = self.get_links(soup)
                all_links.extend(self.compare_set_scraped(page_links))
            except:
                break
                
        with open('links/set_url_ffa.json', 'w') as f:
            json.dump(self.scraped_url, f, indent=4)
        f.close()
        return all_links
    
    def scrap_page(self, soup: BeautifulSoup) -> List[str]:
        """Scrap specific pdf found in a page and return a list of paragraphs.
        """
        par = soup.find('div', class_='field-name-body').find_all('p')
        content = []
        for p in par:
            content.append(self.clean_par(p.text))
        return content
    
    def scrap_pdf(self, soup: BeautifulSoup) -> List[str]:
        """Scrap specific page and return a list of paragraphs.
        """
        pdf_name = self.get_pdf(soup)
        return self.extract_text_pdf(pdf_name)
        
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
    
    def extract_text_pdf(self, pdf_name: str) -> str:
        with open(pdf_name, mode='rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            text = []
            for page in reader.pages[1:-1] :
                text_page = page.extractText()
                text_page = self.clean_pdf_text(text_page)
        f.close()
        return text_page
    
    @staticmethod
    def get_links(soup: BeautifulSoup) -> List[str]:
        list_href = []
        articles = soup.find('div', class_='view-content').find_all('a')
        for article in articles :
            list_href.append('https://www.ffa-assurance.fr' + article.get('href'))
        return list_href
    
    @staticmethod
    def get_pdf(soup: BeautifulSoup) -> str:
        link = soup.find('div', class_='_df_button download').get('source')
        pdf_page = requests.get(link)
        pdf_name = "pdfs/" + link.split('/')[-1]
        pdf = open(pdf_name, 'wb')
        pdf.write(pdf_page.content),
        pdf.close()
        return pdf_name
        
    @staticmethod
    def init_links_memory() -> List[str]: 
        if not os.path.exists('links'):
            os.mkdir('links')
        if not os.path.exists('links/set_url_ffa.json'):
            with open('links/set_url_ffa.json', 'w') as f:
                scraped_url=[]
                json.dump(scraped_url, f)
            f.close()
        else :
            with open('links/set_url_ffa.json', 'r') as f:
                scraped_url = json.load(f)
            f.close()
        return scraped_url
    
    @staticmethod
    def clean_pdf_text(raw_text: str) -> str:
        updated_punc = string.punctuation.replace('\'','').replace('%','')+'˜˚˛˝˙ˆˇ˘'
        text = raw_text.replace('\r','').replace('\n',' ').replace(u"\u2122", '\'')
        ## A changer pour un regex incluant '!' & '?'
        text = text.split('.')
        clean_text = [word.translate(str.maketrans('', '', updated_punc)).lstrip() for word in text]
        return clean_text
    
    @staticmethod
    def clean_par(par: str) -> str:
        cleaned_par = par.replace('\xa0', ' ').replace('(...)', '')
        return cleaned_par