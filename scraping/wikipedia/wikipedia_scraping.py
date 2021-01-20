import wikipedia


class WikipediaScraping:

    def __init__(self, language: str = "fr") -> None:
        self.language = language

        self.undesirable_sections = None
        if self.language == "fr":
            self.undesirable_sections = [
                "== Notes et références ==",
                "== Articles connexes =="
            ]

    def _filter(self, content: str) -> str:
        lines = content.split("\n")

        # remove content of undesirable sections
        if self.undesirable_sections:
            for section in self.undesirable_sections:
                if section in lines:
                    index = lines.index(section)
                    lines = lines[:index]

        # remove section titles
        return " ".join([l for l in lines if l[:2] != "=="])

    def scrap_from_query(self, query: str, limit: int, references: bool = False) -> dict:
        wikipedia.set_lang(self.language)

        output = {}
        query = f"intitle:{query}"
        titles = wikipedia.search(query, results=limit)

        for title in titles:
            content = wikipedia.page(title).content
            filtered_content = self._filter(content)
            output[title.lower()] = {'content': filtered_content}

            if references:
                try:
                    urls_ref = wikipedia.page(title).references
                    output[title.lower()]['references'] = urls_ref
                except Exception:
                    output[title.lower()]['references'] = []

        return output
