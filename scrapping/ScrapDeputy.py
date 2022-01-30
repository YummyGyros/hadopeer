import requests
from bs4 import BeautifulSoup
import json
from os import path

JsonDeputy = "deputy.json"
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

def ScrapSenator(name):
    print(ScrapSenator.first)
    name = name.replace('\xa0', ' ')
    for ch in [';', '.', ',', ':']:
        name = name.replace(ch, "")
    print(name)
    print(ScrapSenator.lst_senator)
    start_json = []
    if name in ScrapSenator.lst_senator:
        return -1
    else:
        ScrapSenator.lst_senator.append(name)
    page = requests.get("https://www.senat.fr/themas/infocompo_2008/infocompo_2008_mono.html")
    soup = BeautifulSoup(page.content, 'html.parser')
    lst_senator = soup.find_all("table")
    lst_name = lst_senator[3].find_all("tr")
    print("receive_name: " + name)
    cutting = name.split(' ')
    print("splitted name: ")
    print(cutting)
    name = cutting[1] + ' ' + cutting[2]
    name = name.lower()
    for senator in lst_name:
        Sname = senator.find_all("p")
        fullname = Sname[0].get_text(strip=True) + ' ' + Sname[1].get_text(strip=True)
        fullname = fullname.lower()
        print (fullname + " " + name)
        if name in fullname:
            if (ScrapSenator.first == True):
                json_senator = {"Name": fullname, "Date_Mandat": "2008-2011", "Dep": Sname[2].get_text(strip=True), "Groupe": Sname[3].get_text(strip=True)}
                start_json.append(json_senator)
                json_senator = json.dumps(start_json, indent=4, separators=(',',': '))
                print(json_senator)
                with open(JsonSenator, 'w') as outfile:
                    outfile.write(json_senator)
                ScrapSenator.first = False
            else:
                with open(JsonSenator) as fp:
                    listObj = json.load(fp)
                listObj.append({"Name": fullname, "Date_Mandat": "2008-2011", "Dep": Sname[2].get_text(strip=True), "Groupe": Sname[3].get_text(strip=True)})
                with open(JsonSenator, 'w') as json_file:
                    json.dump(listObj, json_file, 
                                indent=4,  
                                separators=(',',': '))            
            return 0