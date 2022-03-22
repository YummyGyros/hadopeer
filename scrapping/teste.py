from locale import normalize
from numpy import unicode_
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

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def vote_choice(deputy, choice):
    if (choice.split()[0] == "Pour"):
        return (deputy, "pour")
    if (choice.split()[0] == "Contre"):
        return (deputy, "contre")
    if (choice.split()[0] == "Abstention"):
        return (deputy, "absent")
    return (deputy, "none")

def normalize_list(lst):
    lst_nomalized = []

    for text in lst:
        
        text = strip_accents(text)
        lst_nomalized.append(unicodedata.normalize("NFKD", text))
        print(text)
    print(lst_nomalized)
    return lst_nomalized

def get_vote_deputy(lst_deputy):
    page = requests.get("https://www.assemblee-nationale.fr/13/scrutins/jo0386.asp")
    soup = BeautifulSoup(page.content, 'html.parser')
    lst_vote = []
    i = 0
    lst_i = 0
    lst_deputyV = []
    lst_Normalized = normalize_list(lst_deputy)
    lst_tmp = []

    type_vote = soup.find_all("p", class_="typevote")
    people = soup.find_all("p", class_="noms")
#    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
#    print(people[0].get_text())
#    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    for vote in type_vote:
        lst_deputyV = people[i].get_text().replace(u'\xa0', u' ').split(",")
#        print(lst_deputyV)
        lst_tmp = normalize_list(lst_deputyV)
#        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
#        print(lst_tmp)
#        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        for deputy in lst_tmp:
            if "Mmes" in deputy:
                deputy = deputy[5:]
                lst_deputyV[lst_i] = lst_deputyV[lst_i][5:]
            elif "Mme" in deputy:
                deputy = deputy[4:]
                lst_deputyV[lst_i] = lst_deputyV[lst_i][4:]
            elif "MM." in deputy:
                deputy = deputy[4:]
#                print(deputy)
                lst_deputyV[lst_i] = lst_deputyV[lst_i][4:]
            elif "M." in deputy:
                deputy = deputy[3:]
                lst_deputyV[lst_i] = lst_deputyV[lst_i][3:]
            else:
                deputy = deputy[1:]
                lst_deputyV[lst_i] = lst_deputyV[lst_i][1:]
            if not deputy in lst_Normalized:
                lst_deputy.append(lst_deputyV[lst_i])
#            print(vote)
#            print(deputy)
            lst_vote.append(vote_choice(lst_deputyV[lst_i], vote.get_text(strip=True)))
            lst_i += 1
        lst_i = 0
        i += 1
    return lst_vote

#def detect_debat(url, name):
#    page = requests.get(url)
#    soup = BeautifulSoup(page.content, 'html.parser')
#    field_mandat = soup.find_all("dl", class_="deputes-liste-attributs sycomore")
#    result = []
#    j = []
#    i = 0
#
#    result.append(name)
#    for s in field_mandat:
#        children_field = s.find_all("a")
#        for a in children_field:
#            if a.string and "XIIIe législature" in a.string:
#                mandat = s
#                j = mandat.findChildren("b")
#                result.append(j[0].get_text(strip=True))
#                j = mandat.findChildren("dd")
#                result.append(j[3].get_text(strip=True))
#                result.append(j[4].get_text(strip=True))
#                return result
#            i += 1
#    print(result)
#
#def put_deputy(name, url, state):
#    result = []
#    start_json = []
#    result = detect_debat(url, name)
#    if (state == True):
#        json_deputy = {"name": result[0], "role": "depute", "mandate": result[1], "department": result[2], "politics_group": result[3]}
#        start_json.append(json_deputy)
#        json_deputy = json.dumps(start_json, indent=4, separators=(',',': '))
#        print(json_deputy)
#        with open(JsonDeputy, 'w') as outfile:
#            outfile.write(json_deputy)
#        ScrapDeputy.first = False
#    else:
#        with open(JsonDeputy) as fp:
#            listObj = json.load(fp)
#        listObj.append({"name": result[0], "role": "depute", "mandate": result[1], "department": result[2], "politics_group": result[3]})
#        with open(JsonDeputy, 'w') as json_file:
#            json.dump(listObj, json_file, 
#                        indent=4,  
#                        separators=(',',': '))
#
#def ScrapDeputy(suffix, lst_deputy):
#    page = requests.get("https://www2.assemblee-nationale.fr/sycomore/resultats" + suffix)
#    soup = BeautifulSoup(page.content, 'html.parser')
#    body = soup.find("table", )
#    list_deputy = body.find_all("a", href=True)
#    for deputy in list_deputy:
#        for name in lst_deputy:
#            dep = re.sub(r"(\w)([A-Z])", r"\1 \2", deputy.get_text(strip=True))
#            if name in dep:
#                lst_deputy.remove(name)
#                put_deputy(name, "https://www2.assemblee-nationale.fr" + deputy.get("href"), ScrapDeputy.first)
#    if lst_deputy != []:
#        lis = soup.find_all("div", class_="bottommargin pagination-bootstrap pagination-right pagination-small")
#        suffix = lis[0].find_all("a", href=True)
#        s = suffix[len(suffix) - 1].get("data-uri-suffix")
#        ScrapDeputy.page += 1
#        ScrapDeputy(s, lst_deputy)
#    return 0

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

def put_deputy(name, url, state, lst_vote):
    result = []
    start_json = []
    choice = 0
    acronym = {"La République en Marche" : "RM",
               "Les Républicains" : "R",
               "Mouvement Démocrate (MoDem) et Démocrates apparentés" : "MDD",
               "Socialistes et apparentés" : "SA",
               "Agir ensemble" : "AE",
               "UDI et Indépendants" : "UDII",
               "Libertés et Territoires" : "LT",
               "La France insoumise" : "FI",
               "Gauche démocrate et républicaine" : "GDR",
               "Non inscrit" : "NA"
            }
    result = detect_debat(url, name)
    for name, vote in lst_vote:
        if name in lstdeputy:
            break
        choice += 1

    if (state == True):
        json_deputy = {"name": result[0], "fonction": "depute", "mandat": result[1], "departement": result[2], "groupe_politique": result[3], "scrutin" : [lst_vote[choice][1]]}
        start_json.append(json_deputy)
        json_deputy = json.dumps(start_json, indent=4, separators=(',',': '))
        print(json_deputy)
        with open(JsonDeputy, 'w') as outfile:
            outfile.write(json_deputy)
        ScrapDeputy.first = False
    else:
        with open(JsonDeputy) as fp:
            listObj = json.load(fp)
        listObj.append({"name": result[0], "fonction": "depute", "mandat": result[1], "departement": result[2], "groupe_politique": result[3], "scrutin" : [lst_vote[choice][1]]})
        with open(JsonDeputy, 'w') as json_file:
            json.dump(listObj, json_file, 
                        indent=4,  
                        separators=(',',': '))
    choice = 0

def ScrapDeputy(suffix, lst_deputy):
    lst_vote = get_vote_deputy(lst_deputy)
    page = requests.get("https://www2.assemblee-nationale.fr/sycomore/resultats" + suffix)
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.find("table", )
    list_deputy = body.find_all("a", href=True)
    for deputy in list_deputy:
        for name in lst_deputy:
            dep = re.sub(r"(\w)([A-Z])", r"\1 \2", deputy.get_text(strip=True))
            if name in dep:
                lst_deputy.remove(name)
                put_deputy(name, "https://www2.assemblee-nationale.fr" + deputy.get("href"), ScrapDeputy.first, lst_vote)
    if lst_deputy != []:
        lis = soup.find_all("div", class_="bottommargin pagination-bootstrap pagination-right pagination-small")
        suffix = lis[0].find_all("a", href=True)
        if not suffix[len(suffix) - 1].get_text() == "Suivant":
            return 0
        s = suffix[len(suffix) - 1].get("data-uri-suffix")
        ScrapDeputy.page += 1
        ScrapDeputy(s, lst_deputy)
    return 0

lstdeputy = ["Patrick Roy", "Bernard Accoyer", "Thierry Mariani", "Maxime Gremetz", "Luc Chatel", "Éric Raoult"]
normalize_list(lstdeputy)
ScrapDeputy.first = True
ScrapDeputy.page = 1
ScrapDeputy("", lstdeputy)