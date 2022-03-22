import requests
from bs4 import BeautifulSoup
import json

#from scrapping.ScrapDeputy import JsonSenator

d = {}
d["oui l l"] = [1]
d["oui l l"].append(2)
d["er"] = [1]
d["azs"] = [5]

r = ["Paul"]
s = "paul"

if s in r:
    print("match")

r.remove("Paul")
print(r)

print(d)

if "er" in d:
    print(d)

JsonSenator = "Date_vote.json"

def create_vote_json(lecture):
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
        with open(JsonSenator, 'w') as outfile:
            outfile.write(json_senator)
    else:
        with open(JsonSenator) as fp:
            listObj = json.load(fp)
        listObj.append({"date": name, "assembly" : "Sénat", "number" : lecture})
        with open(JsonSenator, 'w') as json_file:
            json.dump(listObj, json_file, 
                        indent=4,  
                        separators=(',',': '))

for i in [1,2]:
    create_vote_json(i)