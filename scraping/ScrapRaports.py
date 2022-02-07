import json
from bs4 import BeautifulSoup
import requests
from unicodedata import normalize
from ScrapDeputy import ScrapSenator, other_scrap, vote_Senator

tmpFileName = 'tmp.json'

def scrapAssembleeNationale(soup):
    raise Exception("not implemented yet")

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
    lecture = "lecture not mentioned"
    listInterventions = []
    ret = []
    for url in urls :
        if url.find("http://www.senat.fr") != -1:
            interventions = []
            debats = BeautifulSoup(requests.get(url).content, 'html.parser').find("div", {"class": "box-inner gradient-01"})
            intervenant = debats.find_all(
                "div", {"class": "intervenant"})
            for i in intervenant:
                if i.find("span", {"class": "orateur_nom"}) != None:
                    if "président" in i.find("span", {"class": "orateur_nom"}).get_text(strip=True):
                        ScrapSenator(find_president_name(i.find("a", {"class": "lien_senfic"}).get("href")))
                    else:
                        ScrapSenator(i.find("span", {"class": "orateur_nom"}).get_text(strip=True).replace('\n', ' '))
                    interventions.append({
                        "orateur_nom": i.find("span", {"class": "orateur_nom"}).text.replace('\n', ' '),
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
    other_scrap()
    with open(tmpFileName, 'w') as json_file:
        json.dump(ret, json_file,
                  indent=4,
                  separators=(',', ': '))
    return json.dumps(ret, indent=4,
                      separators=(',', ': '))