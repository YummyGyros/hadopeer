
from bs4 import BeautifulSoup, Comment, element
from os import path
import requests
from tqdm import tqdm

article = ''
interventions_senat = []
articles_senat = []
SenatorNom = []

def get_deputi_name(contribution, President):
    ret = ""
    tmp = contribution.text.replace('\n', ' ').replace('\u00a0', ' ').rstrip().lstrip()
    if 'M. le président.' in tmp or 'Mme la présidente' in tmp:
        ret = President
    else:
        if tmp.startswith("M. "):
            ret = tmp.split("M. ")[1].split(".")[0]
        elif tmp.startswith("Mme "):
            ret = tmp.split("Mme ")[1].split(".")[0]
        if ',' in ret:
            ret = ret.split(",")[0]
    return ret

def scrapAN(urls, pb):
    lectures_AN = []
    DeputyNom = []
    for i in tqdm(range(len(urls)), desc="Scraping AN", disable=pb):
        url = urls[i]
        contributions = []
        name = ''
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        President = get_deputi_name(soup.find("h5", {"class": "presidence"}), '')
        titles = soup.find_all("h2", {"class": "titre1"})
        for title in titles:
            for sibling in title.next_siblings:
                if sibling.name == "h2" and 'class' in sibling.attrs:
                    if "titre1" in sibling['class'] :
                        title = sibling.text
                    elif "titre3" in sibling['class'] :
                        President = get_deputi_name(sibling, '')
                elif type(title) == element.Tag:
                    if 'Protection de la création sur Internet' in title.text and sibling.name == "p" and 'class' not in sibling.attrs:
                        txt = sibling.text.replace('\n', ' ').replace('\u00a0', ' ').rstrip().lstrip()
                        if (txt.startswith('M. ')  or txt.startswith('Mme ')) and txt.split(' ')[2].endswith('.'):
                            name = get_deputi_name(sibling, President)
                        if name != '':
                            DeputyNom.append(name)
                            contributions.append({
                                "elected_member": name,
                                "text": txt
                            })
        if contributions != []:
            lectures_AN.append({"date": soup.find("h1", {"class": "seance"}).text.split("du ")[1], "link": url, "contributions": contributions})
    return lectures_AN, DeputyNom


def pagesSenat(url, hadopy):
    global interventions_senat, article, articles_senat, SenatorNom

    intervenants = BeautifulSoup(requests.get(url).content, 'html.parser').find(
        "div", {"class": "box-inner gradient-01"}).find_all(['div', 'p'])
    for intervenant in intervenants:
        if 'class' in intervenant.attrs:
            # if hadopy and intervenant.name == "p" and "mention_article" in intervenant['class']:
            #     if article != '':
            #         articles_senat.append(
            #             {"article": article, "reference": url, "interventions_senat": interventions_senat})
            #         interventions_senat = []
            #     article = intervenant.text.replace('\n', ' ')
            if intervenant.name == "p" and "titre_S1" in intervenant['class'] and 'PRÉSIDENCE' not in intervenant.text and 'Dépôt' not in intervenant.text:
                # if hadopy:
                #     articles_senat.append(
                #         {"article": article, "reference": url, "interventions_senat": interventions_senat})
                #     interventions_senat = []
                hadopy = True if 'protection de la création sur' in intervenant.text else False
            elif hadopy and intervenant.name == "div" and "intervenant" in intervenant['class']:
                orateur = intervenant.find(
                    text=lambda text: isinstance(text, Comment))
                if orateur.string.split(' ')[0] == 'cri:intervenant':
                    SenatorNom.append(orateur.string.split('\"')[3])
                if intervenant.text != "":
                    interventions_senat.append({
                        "elected_member": orateur.string.split('\"')[3] if orateur.string.split(' ')[0] == 'cri:intervenant' else '',
                        "text": intervenant.text.split("\n\n\n\n\n")[0].replace('\n', ' ').replace('\u00a0', ' ').rstrip().lstrip()
                    })
    return hadopy


def scrapSenat(urls, pb):
    hadopy = False
    global interventions_senat, article, articles_senat, SenatorNom

    lectures_senat = []
    premier_interventions_senat = ""

    for i in tqdm(range(len(urls)), desc="Scraping senat", disable=pb):
        url = urls[i]
        interventions_senat = []
        articles_senat = []
        article = ''
        while True:
            hadopy = pagesSenat(url, hadopy)
            soup = BeautifulSoup(requests.get(url).content, 'html.parser')
            if soup.find("a", {"class": "link-next"}) == None:
                break
            url = url.replace(
                url.split('/')[6], '') + soup.find("a", {"class": "link-next"})['href']
        if interventions_senat != []:
            lectures_senat.append({"date": soup.find("h1", {"class": "title-11"}).text.split(
                " (")[0].split("du ")[1], "link": urls[i], "contributions": interventions_senat})
    return lectures_senat, SenatorNom
