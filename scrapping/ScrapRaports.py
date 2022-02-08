
from bs4 import BeautifulSoup, Comment
from os import path
from ScrapDeputy import ScrapSenator, other_scrap, vote_Senator
import requests

def scrapAssembleeNationale(urls):
    # articles = []
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
    ScrapSenator.first = True
    ScrapSenator.lst_senator = []
    vote_Senator.lst_senator = []
    vote_Senator.scrutin = dict()
    vote_Senator.first = 0
    vote_Senator(1)
    vote_Senator(2)
    article = "no mention"
    lecture = "lecture not mentioned"
    articles = []
    lectures_senat = []
    urls = list(dict.fromkeys(urls))
    for url in urls :
        if "http://www.senat.fr" in url:
            interventions = []
            soup = BeautifulSoup(requests.get(url).content, 'html.parser')
            debats = soup.find("div", {"class": "box-inner gradient-01"})
            intervenant = debats.find_all(
                "div", {"class": "intervenant"})
            for i in intervenant:
                if i.find("span", {"class": "orateur_nom"}) != None:
                    orateur = i.find(text=lambda text:isinstance(text, Comment))
                    ScrapSenator(orateur.string.split('\"')[3], vote_Senator.scrutin)
                    interventions.append({
                        # "qualification": orateur.string.split('\"')[5],
                        # "profil": None if i.find("a", {"class": "lien_senfic"}) == None else "http://www.senat.fr" + i.find("a", {"class": "lien_senfic"}).get('href'),
                        "orateur_nom": orateur.string.split('\"')[3],
                        "texte": i.text.split("\n\n\n\n\n")[0].replace('\n', ' ').rstrip().lstrip()
                    }) 
                if i.find("p", {"class": "mention_article"}):
                    articles.append(
                        {"article": article, "reference": url, "interventions": interventions})
                    article = i.find("p", {"class": "mention_article"}).text.replace('\n', ' ')
            articles.append(
                {"article": article, "reference": url, "interventions": interventions})
        else:
            if articles != []:
                lectures_senat.append({"date": lecture.split(" - ")[1], "premier_articles": articles[0]["reference"], "articles": articles})
            lecture = url
    lectures_senat.append({"date": lecture.split(" - ")[1], "premier_articles": articles[0]["reference"], "articles": articles})
    other_scrap(vote_Senator.scrutin)
    return lectures_senat
