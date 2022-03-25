
from faunadb import query as q

from extractScrappedJsons import getDatesLinksFromSessions
from faunaTools import loadJsonArrayFileToFaunaCollection

def createDatesCollection(client):
    contribsPaths = ['../national_assembly_sessions.json', '../senate_sessions.json']
    dates = getDatesLinksFromSessions(contribsPaths)
    client.query(q.create_collection({'name': 'dates'}))
    for elem in dates:
        client.query(q.create(q.collection('dates'), {'data': elem}))

def createCollections(client):
    print("createCollections: code commented for safety reasons")
    createDatesCollection(client)

    # client.query(q.create_collection({'name': 'votes'}))
    # loadJsonArrayFileToFaunaCollection(client, '../votes.json', 'votes')

    # client.query(q.create_collection({'name':'elected_members'}))
    # loadJsonArrayFileToFaunaCollection(client, '../senators.json', 'elected_members')
    # loadJsonArrayFileToFaunaCollection(client, '../deputies.json', 'elected_members')

    # client.query(q.create_collection({'name': 'visualizations'}))