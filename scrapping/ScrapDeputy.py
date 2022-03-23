import requests
from bs4 import BeautifulSoup
import json
from os import path
import unicodedata
import re
from tqdm import tqdm
import re

JsonDeputy = "deputies.json"
JsonSenator = "senators.json"
JsonDate = "votes.json"
listObj = []



def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def create_vote_json_Assembly():
    scrutin = "https://www.assemblee-nationale.fr/13/scrutins/jo0386.asp"
    page = requests.get(scrutin)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find("p", {"class": "entetegeneraliste"})
    name = title.get_text().split('-')[1]
    name = name[11:]


    with open(JsonDate) as fp:
        listObj = json.load(fp)
    listObj.append({"date": name, "assembly" : "Assemblé National", "number" : 1})
    with open(JsonDate, 'w') as json_file:
        json.dump(listObj, json_file, 
                    indent=4,  
                    separators=(',',': '))

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
#        print(text)
#    print(lst_nomalized)
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

def vote_choice(deputy, choice):
    if (choice.split()[0] == "Pour"):
        return (deputy, "pour")
    if (choice.split()[0] == "Contre"):
        return (deputy, "contre")
    if (choice.split()[0] == "Abstention"):
        return (deputy, "absent")
    return (deputy, "none") 

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
#                print(len(j))
                if len(j) < 5:
                    result.append("non-inscrit")
                else:
                    result.append(j[4].get_text(strip=True))
                return result
            i += 1
#    print(result)

def put_deputy(name, url, state, lst_vote):
    result = []
    start_json = []
    choice = 0
    acronym = {"union pour un mouvement populaire" : "UMP",
               "socialiste, radical et citoyen" : "SRC",
               "socialiste" : "SRC",
               "nouveau centre" : "NC",
               "socialiste, radical et citoyen et divers gauche" : "SRC-G",
               "apparent\u00e9 \u00e0 l'union pour un mouvement populaire" : "UMP-A",
               "apparenté union pour un mouvement populaire" : "UMP-A",
               "union pour un mouvement populaire\rgauche d\u00e9mocrate et r\u00e9publicaine\rgauche d\u00e9mocrate et r\u00e9publicaine" : "UMP",
               "apparent\u00e9 socialiste, radical et citoyen et divers gauche" : "SRC-A",
               "apparent\u00e9 nouveau centre" : "NC-A",
               "gauche d\u00e9mocrate et r\u00e9publicaine" : "GDR",
               "d\u00e9put\u00e9s n'appartenant \u00e0 aucun groupe" : "NA",
               "union pour la majorit\u00e9 pr\u00e9sidentielle" : "UMP",
               "non-inscrit" : "NA"
            }
    result = detect_debat(url, name)
    print("list")
    for namee, vote in lst_vote:
        if namee in name:
            break
        choice += 1

    if (state == True):
        json_deputy = {"name": result[0], "job": "depute", "mandate": result[1], "department": result[2], "group": acronym[result[3].lower()], "votes" : [lst_vote[choice][1]]}
        start_json.append(json_deputy)
        json_deputy = json.dumps(start_json, indent=4, separators=(',',': '))
        print(json_deputy)
        with open(JsonDeputy, 'w') as outfile:
            outfile.write(json_deputy)
        ScrapDeputy.first = False
    else:
        print(result)
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print(result[0])
        if result != None:
            with open(JsonDeputy) as fp:
                listObj = json.load(fp)
            listObj.append({"name": result[0], "job": "depute", "mandate": result[1], "department": result[2], "group": acronym[result[3].lower()], "votes" : ["none" if choice >= len(lst_vote) else lst_vote[choice][1]]})
            with open(JsonDeputy, 'w') as json_file:
                json.dump(listObj, json_file, 
                            indent=4,  
                            separators=(',',': '))
    choice = 0

def ScrapDeputy(suffix, lst_deputy, lst_vote):
    if ScrapDeputy.page == 1:
        lst_vote = get_vote_deputy(lst_deputy)
        create_vote_json_Assembly()
    print(lst_deputy)
    print(ScrapDeputy.page)
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
        if not "Suivant" in suffix[len(suffix) - 1].get_text():
            return 0
        s = suffix[len(suffix) - 1].get("data-uri-suffix")
        ScrapDeputy.page += 1
        ScrapDeputy(s, lst_deputy, lst_vote)
    return 0

def create_vote_json_Senat(lecture):
    scrutin = "http://www.senat.fr/scrutin-public/2008/scr2008-30.html" if (lecture == 1) else "http://www.senat.fr/scrutin-public/2008/scr2008-147.html"
    page = requests.get(scrutin)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find("h1", {"class": "title-11"})
    start_json = []
    name = title.get_text().split('-')[1]
    name = name[11:]

    if (lecture == 1):
        json_senator = {"date": name, "assembly" : "Sénat", "number" : lecture}
        start_json.append(json_senator)
        json_senator = json.dumps(start_json, indent=4, separators=(',',': '))
        with open(JsonDate, 'w') as outfile:
            outfile.write(json_senator)
    else:
        with open(JsonDate) as fp:
            listObj = json.load(fp)
        listObj.append({"date": name, "assembly" : "Sénat", "number" : lecture})
        with open(JsonDate, 'w') as json_file:
            json.dump(listObj, json_file, 
                        indent=4,  
                        separators=(',',': '))


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
    create_vote_json_Senat(lecture)
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

def create_vote_json(lecture):
    scrutin = "http://www.senat.fr/scrutin-public/2008/scr2008-30.html" if (lecture == 1) else "http://www.senat.fr/scrutin-public/2008/scr2008-147.html"
    soup = BeautifulSoup(scrutin.content, 'html.parser')

    title = soup.find("h1", {"class": "title-11"})
    start_json = []
    name = title.get_text().split('-')[1]
    name = name[:1]

    if (ScrapSenator.first == True):
        json_senator = {"name": name.get_text(), "senat" : "senat", "number" : lecture}
        start_json.append(json_senator)
        json_senator = json.dumps(start_json, indent=4, separators=(',',': '))
        with open(JsonSenator, 'w') as outfile:
            outfile.write(json_senator)
        ScrapSenator.first = False
    else:
        with open(JsonSenator) as fp:
            listObj = json.load(fp)
        listObj.append({"name": name.get_text(), "senat" : "senat", "number" : lecture})
        with open(JsonSenator, 'w') as json_file:
            json.dump(listObj, json_file, 
                        indent=4,  
                        separators=(',',': '))

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
                json_senator = {"name": name.title(), "job": "senateur", "mandate": "2008-2011", "department": senator_2008[name][0], "group": senator_2008[name][1], "vote": [name_scrutin[0], name_scrutin[1]]}
                start_json.append(json_senator)
                json_senator = json.dumps(start_json, indent=4, separators=(',',': '))
                with open(JsonSenator, 'w') as outfile:
                    outfile.write(json_senator)
                ScrapSenator.first = False
            else:
                with open(JsonSenator) as fp:
                    listObj = json.load(fp)
                listObj.append({"name": name.title(), "job": "senateur", "mandate": "2008-2011", "department": senator_2008[name][0], "group": senator_2008[name][1], "vote": [name_scrutin[0], name_scrutin[1]]})
                with open(JsonSenator, 'w') as json_file:
                    json.dump(listObj, json_file, 
                                indent=4,  
                                separators=(',',': '))            
            return 0