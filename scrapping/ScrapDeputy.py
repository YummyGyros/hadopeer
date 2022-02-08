import requests
from bs4 import BeautifulSoup
import json
from os import path
import unicodedata

JsonDeputy = "deputy.json"
JsonSenator = "senator.json"
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

def vote_Senator(lecture, Name):
    scrutin = "http://www.senat.fr/scrutin-public/2008/scr2008-30.html" if (lecture == 1) else "http://www.senat.fr/scrutin-public/2008/scr2008-147.html"
    page = requests.get(scrutin)

    soup = BeautifulSoup(page.content, 'html.parser')
    if vote_Senator.first < lecture:
        vote_Senator.lst_senator += list(set(get_name_senator(soup)) - set(vote_Senator.lst_senator))
    lst_senator = soup.find_all("table", attrs={'border': '0'})
    lst_name_pour = lst_senator[4].find_all("tr")
    lst_name_contre = lst_senator[5].find_all("tr")
    lst_name_abstention = lst_senator[6].find_all("tr")


    for name in lst_name_pour:
        sname = name.find_all("a")
        for i in range(len(sname)):
            cutting = sname[i].get_text(strip=True).split('\n')
            fullname = cutting[0] + ' ' + cutting[1]
            fullname = fullname.lower()
            if Name in fullname:
                return "pour"
    for name in lst_name_contre:
        sname = name.find_all("a")
        for i in range(len(sname)):
            cutting = sname[i].get_text(strip=True).split('\n')
            fullname = cutting[0] + ' ' + cutting[1]
            fullname = fullname.lower()
            if Name in fullname:
                return "contre"
    for name in lst_name_abstention:
        sname = name.find_all("a")
        for i in range(len(sname)):
            cutting = sname[i].get_text(strip=True).split('\n')
            fullname = cutting[0] + ' ' + cutting[1]
            fullname = fullname.lower()
            if Name in fullname:
                return "absent"
    
    return "None"

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
        json_deputy = {"Name": result[0], "Fonction": "Député", "Date_Mandat": result[1], "Dep": result[2], "Groupe": result[3]}
        start_json.append(json_deputy)
        json_deputy = json.dumps(start_json, indent=4, separators=(',',': '))
        print(json_deputy)
        with open(JsonDeputy, 'w') as outfile:
            outfile.write(json_deputy)
        put_deputy.first = False
    else:
        with open(JsonDeputy) as fp:
            listObj = json.load(fp)
        listObj.append({"Name": result[0], "Fonction": "Député", "Date_Mandat": result[1], "Dep": result[2], "Groupe": result[3]})
        with open(JsonDeputy, 'w') as json_file:
            json.dump(listObj, json_file, 
                        indent=4,  
                        separators=(',',': '))

def ScrapDeputy(name):
    if ScrapDeputy.lst_deputy in name:
        return -1
    else:
        ScrapDeputy.lst_deputy.append(name)
    page = requests.get("https://www2.assemblee-nationale.fr/sycomore/resultats")
    soup = BeautifulSoup(page.content, 'html.parser')
    lst_deputy = soup.find_all("a")

    for deputy in lst_deputy:
        if name in deputy.string:
            put_deputy(name, deputy.get("href"), ScrapDeputy.first)
    return 0

def other_scrap():
    lst_senator = vote_Senator.lst_senator

    for name in ScrapSenator.lst_senator:
        if name in lst_senator:
            lst_senator.remove(name)
    for other in vote_Senator.lst_senator:
        ScrapSenator(other)

def ScrapSenator(name):
    name = name.replace('\xa0', ' ')
    for ch in [';', '.', ',', ':']:
        name = name.replace(ch, "")
    cutting = name.split(' ')
    cutting.pop(0)
    if len(cutting) > 1:
        name = " ".join(cutting)
    name = name.lower()
    if name in ScrapSenator.lst_senator:
        return -1
    else:
        ScrapSenator.lst_senator.append(name)
    start_json = []
    page = requests.get("https://www.senat.fr/themas/infocompo_2008/infocompo_2008_mono.html")
    soup = BeautifulSoup(page.content, 'html.parser')
    lst_senator = soup.find_all("table")
    lst_name = lst_senator[3].find_all("tr")
    for senator in lst_name:
        Sname = senator.find_all("p")
        fullname = Sname[0].get_text(strip=True) + ' ' + Sname[1].get_text(strip=True)
        fullname = fullname.lower()
        if name in fullname:
            if (ScrapSenator.first == True):
                json_senator = {"Name": fullname, "Fonction": "Senateur", "Date_Mandat": "2008-2011", "Dep": Sname[2].get_text(strip=True), "Groupe": Sname[3].get_text(strip=True), "scrutin_1": vote_Senator(1, fullname), "scrutin_2": vote_Senator(2, fullname) }
                start_json.append(json_senator)
                json_senator = json.dumps(start_json, indent=4, separators=(',',': '))
                with open(JsonSenator, 'w') as outfile:
                    outfile.write(json_senator)
                ScrapSenator.first = False
            else:
                with open(JsonSenator) as fp:
                    listObj = json.load(fp)
                listObj.append({"Name": fullname, "Fonction": "Senateur", "Date_Mandat": "2008-2011", "Dep": Sname[2].get_text(strip=True), "Groupe": Sname[3].get_text(strip=True), "scrutin_1": vote_Senator(1, fullname), "scrutin_2": vote_Senator(2, fullname) })
                with open(JsonSenator, 'w') as json_file:
                    json.dump(listObj, json_file, 
                                indent=4,  
                                separators=(',',': '))            
            return 0