import requests
from bs4 import BeautifulSoup
import json
from os import path
import unicodedata
import re
from tqdm import tqdm

JsonDeputy = "deputes.json"
JsonSenator = "senateurs.json"
listObj = []

def get_name_senator(soup):
    lst_senator = soup.find_all("table", attrs={'border': '0'})
    lst_name_pour = lst_senator[4].find_all("tr")
    lst_name_contre = lst_senator[5].find_all("tr")
    lst_name_abstention = lst_senator[6].find_all("tr")
    name_page = []

    for name in lst_name_pour:
        sname = name.find_all("a")
        for i in range(len(sname)):
            cutting = sname[i].get_text(strip=True).split('\n')
            fullname = cutting[0] + ' ' + cutting[1]
            fullname = fullname.lower()
            name_page.append(fullname)
    for name in lst_name_contre:
        sname = name.find_all("a")
        for i in range(len(sname)):
            cutting = sname[i].get_text(strip=True).split('\n')
            fullname = cutting[0] + ' ' + cutting[1]
            fullname = fullname.lower()
            name_page.append(fullname)
    for name in lst_name_abstention:
        sname = name.find_all("a")
        for i in range(len(sname)):
            cutting = sname[i].get_text(strip=True).split('\n')
            fullname = cutting[0] + ' ' + cutting[1]
            fullname = fullname.lower()
            name_page.append(fullname)
    vote_Senator.first += 1
    return name_page

def vote_Senator(lecture):
    tp = ("none", "none")
    scrutin = "http://www.senat.fr/scrutin-public/2008/scr2008-30.html" if (lecture == 1) else "http://www.senat.fr/scrutin-public/2008/scr2008-147.html"
    page = requests.get(scrutin)

    soup = BeautifulSoup(page.content, 'html.parser')
    if vote_Senator.first < lecture:
        vote_Senator.lst_senator += list(set(get_name_senator(soup)) - set(vote_Senator.lst_senator))
    lst_senator = soup.find_all("table", attrs={'border': '0'})
    lst_name_pour = lst_senator[3].find_all("tr")
    lst_name_contre = lst_senator[4].find_all("tr")
    lst_name_abstention = lst_senator[5].find_all("tr")

    for name in lst_name_pour:
        sname = name.find_all("a")
        for i in range(len(sname)):
            cutting = sname[i].get_text(strip=True).split('\n')
            fullname = cutting[0] + ' ' + cutting[1]
            fullname = fullname.lower()
            if not fullname in vote_Senator.scrutin:
                vote_Senator.scrutin[fullname] = list(tp)
            if lecture == 1:
                vote_Senator.scrutin[fullname][0] = "pour"
            else:
                vote_Senator.scrutin[fullname][1] = "pour"
    for name in lst_name_contre:
        sname = name.find_all("a")
        for i in range(len(sname)):
            cutting = sname[i].get_text(strip=True).split('\n')
            fullname = cutting[0] + ' ' + cutting[1]
            fullname = fullname.lower()
            if not fullname in vote_Senator.scrutin:
                vote_Senator.scrutin[fullname] = list(tp)
            if lecture == 1:
                vote_Senator.scrutin[fullname][0] = "contre"
            else:
                vote_Senator.scrutin[fullname][1] = "contre"
    for name in lst_name_abstention:
        sname = name.find_all("a")
        for i in range(len(sname)):
            cutting = sname[i].get_text(strip=True).split('\n')
            fullname = cutting[0] + ' ' + cutting[1]
            fullname = fullname.lower()
            if not fullname in vote_Senator.scrutin:
                vote_Senator.scrutin[fullname] = list(tp)
            if lecture == 1:
                vote_Senator.scrutin[fullname][0] = "absent"
            else:
                vote_Senator.scrutin[fullname][1] = "absent"

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
                # print("-----------------------------------------", j, sep='\n')
                result.append(j[3].get_text(strip=True))
                if len(j) < 5 :
                    result.append("non inscrit")
                else:
                    result.append(j[4].get_text(strip=True))
                return result
            i += 1
    print(result)

def put_deputy(name, url, state):
    result = []
    start_json = []
    result = detect_debat(url, name)
    if (state == True):
        json_deputy = {"name": result[0], "fonction": "depute", "mandat": result[1], "departement": result[2], "groupe_politique": result[3]}
        start_json.append(json_deputy)
        json_deputy = json.dumps(start_json, indent=4, separators=(',',': '))
        # print(json_deputy)
        with open(JsonDeputy, 'w') as outfile:
            outfile.write(json_deputy)
        ScrapDeputy.first = False
    else:
        with open(JsonDeputy) as fp:
            listObj = json.load(fp)
        listObj.append({"name": result[0], "fonction": "depute", "mandat": result[1], "departement": result[2], "groupe_politique": result[3]})
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
        if len(lst_deputy) == 5:
            print(lst_deputy)
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

def take_senator():
    d_senator = dict()

    page = requests.get("https://www.senat.fr/themas/infocompo_2008/infocompo_2008_mono.html")
    soup = BeautifulSoup(page.content, 'html.parser')
    lst_senator = soup.find_all("table")
    lst_name = lst_senator[3].find_all("tr")
    for senator in lst_name:
        Sname = senator.find_all("p")
        fullname = Sname[0].get_text(strip=True) + ' ' + Sname[1].get_text(strip=True)
        fullname = fullname.lower()
        d_senator[fullname] = [Sname[2].get_text(strip=True), Sname[3].get_text(strip=True)]
    return d_senator

def other_scrap(SenatorNom, pb, scrutin):
    ScrapSenator.first = True
    lst_senator_2008 = take_senator()
    SenatorNom = list(set(SenatorNom))

    for i in tqdm(range(len(SenatorNom)), desc="Scraping Senator info", disable=pb):
        ScrapSenator(SenatorNom[i].lower(), scrutin, lst_senator_2008)
    lst_senator = vote_Senator.lst_senator

    for name in SenatorNom:
        if name.lower() in lst_senator:
            lst_senator.remove(name.lower())
    for i in tqdm(range(len(vote_Senator.lst_senator)), desc="other Scraping", disable=pb):
        ScrapSenator(lst_senator[i], scrutin, lst_senator_2008)

def ScrapSenator(name, scrutin, senator_2008):
    name = name.lower()
    if not name in scrutin:
        name_scrutin = ("none", "none")
    else:
        name_scrutin = scrutin[name]
    start_json = []
    for senator in senator_2008:

        if name in senator:

            if (ScrapSenator.first == True):
                json_senator = {"name": name, "fonction": "senateur", "mandat": "2008-2011", "departement": senator_2008[name][0], "groupe_politique": senator_2008[name][1], "scrutins": [name_scrutin[0], name_scrutin[1]]}
                start_json.append(json_senator)
                json_senator = json.dumps(start_json, indent=4, separators=(',',': '))
                with open(JsonSenator, 'w') as outfile:
                    outfile.write(json_senator)
                ScrapSenator.first = False
            else:
                with open(JsonSenator) as fp:
                    listObj = json.load(fp)
                listObj.append({"name": name, "fonction": "senateur", "mandat": "2008-2011", "departement": senator_2008[name][0], "groupe_politique": senator_2008[name][1], "scrutins": [name_scrutin[0], name_scrutin[1]]})
                with open(JsonSenator, 'w') as json_file:
                    json.dump(listObj, json_file, 
                                indent=4,  
                                separators=(',',': '))            
            return 0