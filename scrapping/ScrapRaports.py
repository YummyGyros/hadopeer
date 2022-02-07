
from bs4 import BeautifulSoup, Comment
from os import path
from ScrapDeputy import ScrapSenator, other_scrap, vote_Senator
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

def find_president_name(url):
    suite = url.split("/")
    page = requests.get("http://www.senat.fr/senateur/" + suite[2])
    soup = BeautifulSoup(page.content, 'html.parser')
    soup.prettify("latin-1")
    title = soup.find("h1", {"class": "title-01"}).get_text(strip=True)
    splitting = title.split(" ")
    if "M." in splitting or "Mme." in splitting:
        title = "Mme " + splitting[1] + " " + splitting[2]
    else:
        title = "Mme " + splitting[1] + " " + splitting[0]
    return title

def scrapSenat(urls):
    ScrapSenator.first = True
    ScrapSenator.lst_senator = []
    vote_Senator.lst_senator = []
    vote_Senator.first = 0
    mention = "no mention"
    articles = "articles not mentioned"
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
                    print(orateur.string.split('\"')[3])
                    if "président" in i.find("span", {"class": "orateur_nom"}).get_text(strip=True):
                        ScrapSenator(find_president_name(i.find("a", {"class": "lien_senfic"}).get("href")))
                    else:
                        ScrapSenator(i.find("span", {"class": "orateur_nom"}).get_text(strip=True).replace('\n', ' '))
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
                ret.append({"title": articles, "articles": listInterventions})
            articles = url
    ret.append({"title": articles, "articles": listInterventions})
    other_scrap()
    return ret
