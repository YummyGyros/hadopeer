import jsonTools
import dateparser
from faunadb import query as q

sessionsPaths = ['../national_assembly_sessions.json', '../senate_sessions.json']
senatePaths = ['../senate_sessions.json']
natAssemblyPaths = ['../national_assembly_sessions.json']

membersPaths = ['../senators.json', '../deputies.json']
senatorsPaths = ['../senators.json']
deputiesPaths = ['../deputies.json']

def getAllContributions(filepaths):
    for path in filepaths:
        objects = jsonTools.getObjectFromJsonFile(path)
        contribs = []
        for object in objects:
            for contrib in object['contributions']:
                contribs.append(contrib['text'])
    return contribs

def getAllDateContributions(filepaths):
    tuples = []
    for path in filepaths:
        objects = jsonTools.getObjectFromJsonFile(path)
        for object in objects:
            tuple = (object['date'], [])
            for contrib in object['contributions']:
                tuple[1].append(contrib['text'])
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

def getContributionsSamples(client):
    samples = []
    tuple = ('all', getAllContributions(sessionsPaths))
    samples.append(tuple)
#    tuple = ('national_assembly', getAllContributions(natAssemblyPaths))
#    samples.append(tuple)
#    tuple = ('senate', getAllContributions(senatePaths))
#    samples.append(tuple)
#    groups = client.query(q.paginate(q.match(q.index('elected_members_group'))))['data']
#    for group in groups:
#        contribs = getContribsFromMatchingMembers(sessionsPaths, membersPaths, 'group', group)
#        tuple = (group, contribs)
#        samples.append(tuple)
    return samples

def getDateContributionsSamples(client):
    samples = []
    tuple = ('all', getAllDateContributions(sessionsPaths))
    samples.append(tuple)
#    tuple = ('national_assembly', getAllDateContributions(natAssemblyPaths))
#    samples.append(tuple)
#    tuple = ('senate', getAllDateContributions(senatePaths))
#    samples.append(tuple)
    # groups = client.query(q.paginate(q.match(q.index('elected_members_group'))))['data']
    # for group in groups:
    #     contribs = getContribsFromMatchingMembers(sessionsPaths, membersPaths, 'group', group)
    #     tuple = (group, contribs)
    #     samples.append(tuple)
    return samples