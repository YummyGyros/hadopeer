
from faunadb import query as q

from extractScrappedJsons import getDatesLinksFromSessions
from faunaTools import loadJsonArrayFileToFaunaCollection

def createDatesCollection(client):
    contribsPaths = ['national_assembly_sessions.json', 'senate_sessions.json']
    for i in range(len(contribsPaths)):
        contribsPaths[i] = '../save_test_db_json/' + contribsPaths[i]
    dates = getDatesLinksFromSessions(contribsPaths)
    client.query(q.create_collection({'name': 'dates'}))
    for elem in dates:
        client.query(q.create(q.collection('dates'), {'data': elem}))

def createCollections(client):
    createDatesCollection()
    client.query(q.create_collection({'name': 'votes'}))
    loadJsonArrayFileToFaunaCollection(client, '../votes.json', 'votes')
    client.query(q.create_collection({'name':'elected_members'}))
    loadJsonArrayFileToFaunaCollection('../senators.json', 'elected_members')
    loadJsonArrayFileToFaunaCollection('../deputies.json', 'elected_members')
    client.query(q.create_collection({'name': 'visualizations'}))