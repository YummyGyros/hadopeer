import requests
from bs4 import BeautifulSoup
import json
from os import path
import unicodedata
from tqdm import tqdm
import re

JsonDeputy = "deputies.json"
JsonSenator = "senator.json"
listObj = []

def detect_debat(url, name):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    field_mandat = soup.find_all("dl", class_="deputes-liste-attributs sycomore")
    result = []
    j = []
    i = 0

    result.append(name)
    for s in field_mandat:
        children_field = s.find_all("a")
        for a in children_field:
            if a.string and "XIIIe législature" in a.string:
                mandat = s
                j = mandat.findChildren("b")
                result.append(j[0].get_text(strip=True))
                j = mandat.findChildren("dd")
                result.append(j[3].get_text(strip=True))
                result.append(j[4].get_text(strip=True))
                return result
            i += 1
    print(result)

def put_deputy(name, url, state):
    result = []
    start_json = []
    result = detect_debat(url, name)
    if (state == True):
        json_deputy = {"name": result[0], "role": "depute", "mandate": result[1], "department": result[2], "politics_group": result[3]}
        start_json.append(json_deputy)
        json_deputy = json.dumps(start_json, indent=4, separators=(',',': '))
        print(json_deputy)
        with open(JsonDeputy, 'w') as outfile:
            outfile.write(json_deputy)
        ScrapDeputy.first = False
    else:
        with open(JsonDeputy) as fp:
            listObj = json.load(fp)
        listObj.append({"name": result[0], "role": "depute", "mandate": result[1], "department": result[2], "politics_group": result[3]})
        with open(JsonDeputy, 'w') as json_file:
            json.dump(listObj, json_file, 
                        indent=4,  
                        separators=(',',': '))

def ScrapDeputy(suffix, lst_deputy):
    page = requests.get("https://www2.assemblee-nationale.fr/sycomore/resultats" + suffix)
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.find("table", )
    list_deputy = body.find_all("a", href=True)
    for deputy in list_deputy:
        for name in lst_deputy:
            dep = re.sub(r"(\w)([A-Z])", r"\1 \2", deputy.get_text(strip=True))
            if name in dep:
                lst_deputy.remove(name)
                put_deputy(name, "https://www2.assemblee-nationale.fr" + deputy.get("href"), ScrapDeputy.first)
    if lst_deputy != []:
        lis = soup.find_all("div", class_="bottommargin pagination-bootstrap pagination-right pagination-small")
        suffix = lis[0].find_all("a", href=True)
        s = suffix[len(suffix) - 1].get("data-uri-suffix")
        ScrapDeputy.page += 1
        ScrapDeputy(s, lst_deputy)
    return 0

lstdeputy = ["Patrick Roy", "Bernard Accoyer", "Thierry Mariani", "Maxime Gremetz", "Luc Chatel"]
ScrapDeputy.first = True
ScrapDeputy.page = 1
ScrapDeputy("", lstdeputy)