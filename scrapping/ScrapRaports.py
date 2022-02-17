
from bs4 import BeautifulSoup, Comment
from os import path 
import requests
from tqdm import tqdm


def scrapAssembleeNationale(urls):
    # articles = []
    # ret = []
    # for url in urls :
    #     interventions = []
    #     debats = BeautifulSoup(requests.get(url).content, 'html.parser')
    #     intervenants = debats.find_all("span", {"style": "font-family: 'Times New Roman'; font-size: 13pt"})
    #     for i in intervenants:
    #         if 'M' in i:
    #             print(i)
    return([])

def scrapSenat(urls, pb):
    SenatorNom = []
    article = lecture = "not mentioned"
    articles = []
    lectures_senat = []
    urls = list(dict.fromkeys(urls))
    for i in tqdm(range(len(urls)), desc="Scraping debat", disable=pb):
        if "http://www.senat.fr" in urls[i]:
            interventions = []
            soup = BeautifulSoup(requests.get(urls[i]).content, 'html.parser')
            debats = soup.find("div", {"class": "box-inner gradient-01"})
            intervenants = debats.find_all(
                "div", {"class": "intervenant"})
            for intervenant in intervenants:
                if intervenant.find("span", {"class": "orateur_nom"}) != None:
                    orateur = intervenant.find(
                        text=lambda text: isinstance(text, Comment))
                    SenatorNom.append(orateur.string.split('\"')[3])
                    interventions.append({
                        # "qualification": orateur.string.split('\"')[5],
                        # "profil": None if intervenant.find("a", {"class": "lien_senfic"}) == None else "http://www.senat.fr" + intervenant.find("a", {"class": "lien_senfic"}).get('href'),
                        "orateur_nom": orateur.string.split('\"')[3],
                        "texte": intervenant.text.split("\n\n\n\n\n")[0].replace('\n', ' ').rstrip().lstrip()
                    })
                if intervenant.find("p", {"class": "mention_article"}):
                    articles.append(
                        {"article": article, "reference": urls[i], "interventions": interventions})
                    article = intervenant.find(
                        "p", {"class": "mention_article"}).text.replace('\n', ' ')
                    interventions = []
            articles.append(
                {"article": article, "reference": urls[i], "interventions": interventions})
        else:
            if articles != []:
                lectures_senat.append({"date": lecture.split(
                    " - ")[1], "premier_articles": articles[0]["reference"], "articles": articles})
                articles = []
            lecture = urls[i]
    lectures_senat.append({"date": lecture.split(
        " - ")[1], "premier_articles": articles[0]["reference"], "articles": articles})
    return lectures_senat, SenatorNom
