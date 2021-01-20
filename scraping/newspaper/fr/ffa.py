import json
import os
import string
from typing import List, Tuple, Dict

import PyPDF2
import bs4
import requests
from bs4 import BeautifulSoup


class FfaScraping:

    def __init__(self, keywords: List[Tuple], memory: bool = False) -> None:
        """Scrap articles from Atlas Magazine. Set a number of keywords as well
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
            if soup.find('div', class_='_df_button download') is not None:
                content.extend(self.scrap_pdf(soup))
            else:
                content.extend(self.scrap_page(soup))
        return content

    def get_all_links(self, keyword: str, nb_pages: int) -> List[str]:
        """Iterate through number of pages defined by `keyword`, 
        and retrieve links of articles to scrap.
        """
        links = []
        for i in range(0, nb_pages + 1):
            url = f'https://www.ffa-assurance.fr/search?search_api_views_fulltext={keyword}&type=2&page={i}'
            try:
                soup = bs4.BeautifulSoup(requests.get(url).text)
                page_links = self.get_links(soup)
                links.extend(self.compare_set_scraped(page_links))
            except Exception:
                break

        if self.memory:
            with open('links/set_url_ffa.json', 'w') as f:
                json.dump(self.scraped_url, f, indent=4)

        return links

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
        """Verifying that a link retrieved for a keyword was not precedently retrieved by an other keyword
            - links : list of retrieved url to inspect
        """
        intersect = list(set(self.scraped_url).intersection(links))
        links = list(set(links))

        if len(intersect) > 0:
            for i in intersect:
                links.remove(i)
        self.scraped_url.extend(links)

        return links

    def extract_text_pdf(self, pdf_name: str) -> List[str]:
        with open(pdf_name, mode='rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            for page in reader.pages[1:-1]:
                text_page = page.extractText()
                text_page = self.clean_pdf_text(text_page)
        return text_page

    def init_links_memory(self) -> List[str]:
        scraped_url = []

        if self.memory:

            if not os.path.exists('links'):
                os.mkdir('links')

            if not os.path.exists('links/set_url_ffa.json'):
                with open('links/set_url_ffa.json', 'w') as f:
                    json.dump(scraped_url, f)
            else:
                with open('links/set_url_ffa.json', 'r') as f:
                    scraped_url = json.load(f)

        return scraped_url

    @staticmethod
    def get_links(soup: BeautifulSoup) -> List[str]:
        list_href = []
        articles = soup.find('div', class_='view-content').find_all('a')
        for article in articles:
            list_href.append('https://www.ffa-assurance.fr' + article.get('href'))
        return list_href

    @staticmethod
    def get_pdf(soup: BeautifulSoup) -> str:
        link = soup.find('div', class_='_df_button download').get('source')
        pdf_page = requests.get(link)
        pdf_name = "pdfs/" + link.split('/')[-1]

        with open(pdf_name, 'wb') as pdf:
            pdf.write(pdf_page.content)

        return pdf_name

    @staticmethod
    def clean_pdf_text(raw_text: str) -> List[str]:
        updated_punc = string.punctuation.replace('\'', '').replace('%', '') + '˜˚˛˝˙ˆˇ˘'
        text = raw_text.replace('\r', '').replace('\n', ' ').replace(u"\u2122", '\'')
        ## A changer pour un regex incluant '!' & '?'
        text = text.split('.')
        clean_text = [word.translate(str.maketrans('', '', updated_punc)).lstrip() for word in text]
        return clean_text

    @staticmethod
    def clean_par(par: str) -> str:
        cleaned_par = par.replace('\xa0', ' ').replace('(...)', '')
        return cleaned_par
