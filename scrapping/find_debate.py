import requests
from bs4 import BeautifulSoup


def find_debate(url_senat, url_AN):
    urlSenat = []
    urlAN = []

    for fieldset in BeautifulSoup(requests.get(url_senat).content, 'html.parser').find_all("fieldset", class_="lecture lecture-senat"):
        urlSenat.append("http://www.senat.fr" + BeautifulSoup(requests.get("http://www.senat.fr/" + fieldset.find(text="Compte rendu intégral des débats")
                        .parent['href']).content, 'html.parser').find("div", {"class": "box-inner gradient-01"}).find(text="Discussion générale").parent['href'].split("#")[0])
    urlSenat.insert(
        1, "http://www.senat.fr/seances/s200810/s20081030/s20081030001.html")  # temp

    for i in BeautifulSoup(requests.get(url_AN).content, 'html.parser').find_all("font", text="Discussion en séance publique"):
        tab = i.find_next("table")
        for tr in tab.find_all("tr"):
            font = tr.find("font")
            if font != None and font["face"] == "Arial" and font["size"] == "2":
                urlAN.append('https://www.assemblee-nationale.fr' +
                             font.contents[1]['href'])
    urlAN = list(dict.fromkeys(urlAN))
    return urlSenat, urlAN
