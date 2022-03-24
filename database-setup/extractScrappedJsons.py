import jsonTools
import dateparser
from faunadb import query as q

sessionsPaths = ['../national_assembly_sessions.json', '../senate_sessions.json']
membersPaths = ['../senators.json', '../deputies.json']

def getAllContributions(filepaths):
    for path in filepaths:
        objects = jsonTools.getObjectFromJsonFile(path)
        contribs = []
        for object in objects:
            for contrib in object['contributions']:
                contribs.append(contrib['text'])
    return contribs

def getAllDateContributions(filepaths):
    for path in filepaths:
        objects = jsonTools.getObjectFromJsonFile(path)
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
        members = jsonTools.getObjectFromJsonFile(path)
        for member in members:
            if member[field] == value:
                names.append(member['name'])
    # get contribs from names
    for path in contribsPaths:
        objects = jsonTools.getObjectFromJsonFile(path)
        for obj in objects:
            for contrib in obj['contributions']:
                if (name == obj['elected_member'] for name in names):
                    contribs.append(contrib['text'])

def getDatesLinksFromSessions(filepaths):
    datesLinks = []
    for path in filepaths:
        objects = jsonTools.getObjectFromJsonFile(path)
        for obj in objects:
            if (obj['date'] != dateLink[0] or obj['link'] != dateLink[1] for dateLink in datesLinks):
                date = dateparser.parse(obj['date']).date().strftime("%Y-%m-%d")
                datesLinks.append({ 'date': q.date(date), 'link': obj['link']})
    return datesLinks

def getContributionsGroups():
    groups = []
    groups.append(getAllContributions(sessionsPaths))
    # groups.append(getContribsFromMatchingMembers(sessionsPaths, membersPaths, 'job', 'sénateur'))
    # groups.append(getContribsFromMatchingMembers(sessionsPaths, membersPaths, 'job', 'député'))
    # groups = client.query(q.paginate(q.match(q.index('elected_members_group'))))['data']
    return groups

def getDateContributionsGroups():
    groups = []
    groups.append(getAllDateContributions(sessionsPaths))
    return groups

# ISSUES:
#   - fonction très proche des autres: meilleure archi?
#   - peu opti: pour les sessions du sénat, compare avec sénateurs et députés actuellement
#   - recup DateContribs?
#   - filtre soit Sénat soit UMP mais comment filtrer Sénat ET UMP (car groupe existe a l'AN aussi)