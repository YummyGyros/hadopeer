import requests
from bs4 import BeautifulSoup

def parse_site(url):
    page = requests.get(url)
    article = []

    soup = BeautifulSoup(page.content, 'html.parser')
    article.append(soup.find("h2", class_="title-11"))
    Article = soup.findAll("a", class_='titreart')
    for i in Article:
        if "Article" in i.string:
            if not 'avant' in i.string:
                article.append(i)
    return article

def main(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    field_senat = soup.find_all("fieldset", class_="lecture lecture-senat")
    field_an = soup.find_all("fieldset", class_="lecture lecture-an")
    link = []
    result = []

    for s in field_senat:
        children_field = s.findChildren("a")
        for a in children_field:
            if a.string and "Compte rendu intégral des débats" in a.string:
                link.append(a.get("href"))
    for s in field_an:
        children_field = s.findChildren("a")
        for a in children_field:
            if a.string and "Rapport" in a.string:
                result.append(a)
    for url in link:
        result.append(parse_site("http://www.senat.fr/" + url))
    return result

main("http://www.senat.fr/dossier-legislatif/pjl07-405.html")