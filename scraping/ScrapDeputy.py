import requests
from bs4 import BeautifulSoup
import json
from os import path

JsonDeputy = "deputy.json"
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
        print(s)
        print("dino nuggies")
        for a in children_field:
            if a.string and "XIIIe législature" in a.string:
                good = True
                mandat = s
                j = mandat.findChildren("b")
                result.append(j[0].get_text(strip=True))
                j = mandat.findChildren("dd")
                result.append(j[3].get_text(strip=True))
                result.append(j[4].get_text(strip=True))
                print(result)
                return result
            i += 1
    print(result)

def put_deputy(name, url, state):
    result = []
    start_json = []
    result = detect_debat(url, name)
    if (state == True):
        json_deputy = {"Name": result[0], "Date_Mandat": result[1], "Dep": result[2], "Groupe": result[3]}
        start_json.append(json_deputy)
        json_deputy = json.dumps(start_json, indent=4, separators=(',',': '))
        print(json_deputy)
        with open(JsonDeputy, 'w') as outfile:
            outfile.write(json_deputy)
        put_deputy.first = False
    else:
        with open(JsonDeputy) as fp:
            listObj = json.load(fp)
        listObj.append({"Name": result[0], "Date_Mandat": result[1], "Dep": result[2], "Groupe": result[3]})
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
