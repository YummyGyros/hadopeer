import jsonTools
import dateparser
from faunadb import query as q

sessionsPaths = ['../senate_sessions.json', '../national_assembly_sessions.json']
senatePaths = ['../senate_sessions.json']
natAssemblyPaths = ['../national_assembly_sessions.json']

membersPaths = ['../senators.json', '../deputies.json']
senatorsPaths = ['../senators.json']
deputiesPaths = ['../deputies.json']

# get contributions
def appendTextFromContrib(contribs, object):
    for contrib in object['contributions']:
        contribs.append(contrib['text'])

def appendDateTextFromContrib(tuples, object):
    tuple = (object['date'], [])
    for contrib in object['contributions']:
        tuple[1].append(contrib['text'])
    tuples.append(tuple)

def getContributions(filepaths, appender):
    contribs = []
    for path in filepaths:
        objects = jsonTools.getObjectFromJsonFile(path)
        for object in objects:
            appender(contribs, object)
    return contribs

# get matching contributions
def appendMatchingText(contribs, names, object):
    for contrib in object['contributions']:
        for name in names:
            if name == contrib['elected_member']:
                contribs.append(contrib['text'])

def appendMatchingDateText(tuples, names, object):
    tuple = (object['date'], [])
    for contrib in object['contributions']:
        for name in names:
            if name == contrib['elected_member']:
                tuple[1].append(contrib['text'])
    if not list == []:
        tuples.append(tuple)

def getMembersContribs(contribsPaths, membersPaths, field, value, matchingAppender):
    names = []
    contribs = []
    for path in membersPaths:
        members = jsonTools.getObjectFromJsonFile(path)
        for member in members:
            if member[field] == value:
                names.append(member['name'])
    for path in contribsPaths:
        objects = jsonTools.getObjectFromJsonFile(path)
        for object in objects:
            matchingAppender(contribs, names, object)
    return contribs

# get samples
def getLambdaContribSamples(client, appender, matchingAppender):
    samples = []
    tuple = ('all', getContributions(sessionsPaths, appender))
    samples.append(tuple)
    # tuple = ('assemblée nationale', getContributions(natAssemblyPaths, appender))
    # samples.append(tuple)
    # tuple = ('sénat', getContributions(senatePaths, appender))
    # samples.append(tuple)
    # match = q.match(q.index('elected_members_group'))
    # groups = client.query(q.paginate(q.distinct(match)))['data']
    # for group in groups:
    #     contribs = getMembersContribs(sessionsPaths, membersPaths,
    #         'group', group, matchingAppender)
    #     samples.append((group, contribs))
    return samples

def getContribSamples(client):
    return getLambdaContribSamples(
        client, appendTextFromContrib, appendMatchingText
    )

def getDateContribSamples(client):
    return getLambdaContribSamples(
        client, appendDateTextFromContrib, appendMatchingDateText
    )

# get dates links
def getDatesLinksFromSessions(filepaths):
    datesLinks = []
    for path in filepaths:
        objects = jsonTools.getObjectFromJsonFile(path)
        for obj in objects:
            if (obj['date'] != dateLink[0] or obj['link'] != dateLink[1] for dateLink in datesLinks):
                date = dateparser.parse(obj['date']).date().strftime("%Y-%m-%d")
                datesLinks.append({ 'date': q.date(date), 'link': obj['link']})
    return datesLinks