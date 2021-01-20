from l_agefi import LAgefiScraping
from ouest_france import OuestFranceScraping
from universite_assurance import UniversiteAssuranceScraping
from assurland import AssurlandScraping
from l_obs import LObsScraping
from risques import RisquesScraping
from tribune_assurance import TribuneAssuranceScraping
from l_opinion import LOpinionScraping
from le_figaro import LeFigaroScraping
from le_monde import LeMondeScraping
from marianne import MarianneScraping
from atlas_magazine import AtlasMagazineScraping
import json

class Scraper:

    def __init__(self, keywords, nb_pages):
        if nb_pages is None:

    def __init__(self.)
    
    def scrap_agefi(self):
        agefi_scraper = LAgefiScraping(self.keywords)
        open('scrapped/l_agrefi.json', 'w') as f:
            json.dump(agefi_scraper.scrap() , f, indent=4)
        f.close()
    
    def ouest_france(self):
        ouest_france_scraper = OuestFranceScraping(self.keywords)
        open('scrapped/ouest_france.json', 'w') as f:
            json.dump(ouest_france_scraper.scrap() , f, indent=4)
        f.close()

    def universite_assurance(self):
        universite_assurance_scraper = UniversiteAssuranceScraping(self.keywords)
        open('scrapped/universite_assurance.json', 'w') as f:
            json.dump(universite_assurance_scraper.scrap() , f, indent=4)
        f.close()

    def assurland_france(self):
        assurland_france_scraper = AssurlandScraping(self.keywords)
        open('scrapped/assurland.json', 'w') as f:
            json.dump(assurland_scraper.scrap() , f, indent=4)
        f.close()

    def l_obs(self):
        l_obs_scraper = LObsScraping(self.keywords)
        open('scrapped/l_obs.json', 'w') as f:
            json.dump(l_obs_scraper.scrap() , f, indent=4)
        f.close()

    def risques(self):
        risques_scraper = RisquesScraping(self.keywords)
        open('scrapped/risques.json', 'w') as f:
            json.dump(risques_scraper.scrap() , f, indent=4)
        f.close()

    def tribune_assurance(self):
        tribune_assurance_scraper = TribuneAssuranceScraping(self.keywords)
        open('scrapped/tribune_assurance.json', 'w') as f:
            json.dump(tribune_assurance_scraper.scrap() , f, indent=4)
        f.close()

    def l_opinion(self):
        l_opinion_scraper = LOpinionScraping(self.keywords)
        open('scrapped/l_opinion.json', 'w') as f:
            json.dump(l_opinion_scraper.scrap() , f, indent=4)
        f.close()

    def le_figaro(self):
        le_figaro_scraper = LeFigaroScraping(self.keywords)
        open('scrapped/le_figaro.json', 'w') as f:
            json.dump(le_figaro_scraper.scrap() , f, indent=4)
        f.close()

    def le_monde(self):
        le_monde_scraper = LeMondeScraping(self.keywords)
        open('scrapped/le_monde.json', 'w') as f:
            json.dump(le_monde_scraper.scrap() , f, indent=4)
        f.close()

    def marianne(self):
        marianne_scraper = MarianneScraping(self.keywords)
        open('scrapped/marianne.json', 'w') as f:
            json.dump(marianne.scrap() , f, indent=4)
        f.close()

    def atlas_magazine(self):
        atlas_magazine_scraper = AtlasMagazineScraping(self.keywords)
        open('scrapped/atlas_magazine.json', 'w') as f:
            json.dump(atlas_magazine_scraper.scrap() , f, indent=4)
        f.close()


    def ffa(self):
        ffa_scraper = FfaScraping(self.keywords)
        open('scrapped/ffa.json', 'w') as f:
            json.dump(ffa_scraper.scrap() , f, indent=4)
        f.close()