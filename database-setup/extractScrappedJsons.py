import jsonTools
import dateparser
from faunadb import query as q

def getAllContributions(filepaths):
    for path in filepaths:
        objects = jsonTools.getObjectFromJsonArrayFile(path)
        contribs = []
        for object in objects:
            for contrib in object['contributions']:
                contribs.append(contrib['text'])
    return contribs

def getAllDateContributions(filepaths):
    for path in filepaths:
        objects = jsonTools.getObjectFromJsonArrayFile(path)
        tuples = []
        for object in objects:
            tuple = (object['date'], [])
            for contrib in object['contributions']:
                tuple[1].append(contrib['text'])
                break
            tuples.append(tuple)
    return tuples


def getContribsFromMatchingMembers(contribsPaths, membersPaths, field, value):
    # select names
    names = []
    contribs = []
    for path in membersPaths:
        members = jsonTools.getObjectFromJsonArrayFile(path)
        for member in members:
            if member[field] == value:
                names.append(member['name'])
    # get contribs from names
    for path in contribsPaths:
        objects = jsonTools.getObjectFromJsonArrayFile(path)
        for obj in objects:
            for contrib in obj['contributions']:
                if (name == obj['elected_member'] for name in names):
                    contribs.append(contrib['text'])

def getDatesLinksFromSessions(filepaths):
    datesLinks = []
    for path in filepaths:
        objects = jsonTools.getObjectFromJsonArrayFile(path)
        for obj in objects:
            if (obj['date'] != dateLink[0] or obj['link'] != dateLink[1] for dateLink in datesLinks):
                date = dateparser.parse(obj['date']).date().strftime("%Y-%m-%d")
                datesLinks.append({ 'date': q.date(date), 'link': obj['link']})
    return datesLinks


# ISSUES:
#   - fonction très proche des autres: meilleure archi?
#   - peu opti: pour les sessions du sénat, compare avec sénateurs et députés actuellement
#   - recup DateContribs?
#   - filtre soit Sénat soit UMP mais comment filtrer Sénat ET UMP (car groupe existe a l'AN aussi)