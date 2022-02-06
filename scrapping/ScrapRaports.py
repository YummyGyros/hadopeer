
from bs4 import BeautifulSoup, Comment
from os import path
from ScrapDeputy import ScrapSenator
import requests

def scrapAssembleeNationale(urls):
    # listInterventions = []
    # ret = []
    # for url in urls :
    #     interventions = []
    #     debats = BeautifulSoup(requests.get(url).content, 'html.parser')
    #     intervenant = debats.find_all("span", {"style": "font-family: 'Times New Roman'; font-size: 13pt"})
    #     for i in intervenant:
    #         if 'M' in i:
    #             print(i)
    return([])


def scrapSenat(urls):
    mention = "no mention"
    lecture = "lecture not mentioned"
    listInterventions = []
    ret = []
    for url in urls :
        if "http://www.senat.fr" in url:
            interventions = []
            debats = BeautifulSoup(requests.get(url).content, 'html.parser').find("div", {"class": "box-inner gradient-01"})
            intervenant = debats.find_all(
                "div", {"class": "intervenant"})
            for i in intervenant:
                if i.find("span", {"class": "orateur_nom"}) != None:
                    orateur = i.find(text=lambda text:isinstance(text, Comment))
                    # ScrapSenator(orateur.string.split('\"')[3])
                    interventions.append({
                        "qualification": orateur.string.split('\"')[5],
                        "href": None if i.find("a", {"class": "lien_senfic"}) == None else "http://www.senat.fr" + i.find("a", {"class": "lien_senfic"}).get('href'),
                        "orateur_nom": orateur.string.split('\"')[3],
                        "text": i.text.split("\n\n\n\n\n")[0].replace('\n', ' ').rstrip().lstrip() # .encode('ascii', 'ignore').decode()
                    }) 
                if i.find("p", {"class": "mention_article"}):
                    listInterventions.append(
                        {"mention_article": mention, "interventions": interventions})
                    mention = i.find("p", {"class": "mention_article"}).text.replace('\n', ' ')
            listInterventions.append(
                {"mention_article": mention, "interventions": interventions})
        else:
            if listInterventions != []:
                ret.append({"title": lecture, "lecture": listInterventions})
            lecture = url
    ret.append({"title": lecture, "lecture": listInterventions})
    return ret
