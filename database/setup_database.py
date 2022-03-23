import os
import json
import sys
import dateparser
from urllib.parse import urlparse
from faunadb import query as q
from faunadb.client import FaunaClient
import jsonTools
import warnings
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)

secret = os.getenv("FAUNADB_SECRET")
endpoint = os.getenv("FAUNADB_ENDPOINT")

if not secret:
  print("The FAUNADB_SECRET environment variable is not set, exiting.")
  sys.exit(1)

endpoint = endpoint or "https://db.fauna.com/"
o = urlparse(endpoint)

client = FaunaClient(
  secret=secret,
  domain=o.hostname,
  port=o.port,
  scheme=o.scheme
)

def tryAddTextToExistingElem(date, member, text, objects):
  for object in objects:
    if q.equals(object['date'], date):
      if object['elected_member'] == member:
        object['text'].append(text)
        return True
  return False

def loadContributionsCollectionFromSessions(collection, filepath):
  rawFileData = open(filepath, 'r')
  jsonFileData = json.load(rawFileData)
  objects = []
  for elem in jsonFileData:
    for contrib in elem['contributions']:
      if not tryAddTextToExistingElem(elem['date'], contrib['elected_member'], contrib['text'], objects):
        date = dateparser.parse(elem['date']).date().strftime("%Y-%m-%d")
        object = {
          'elected_member': contrib['elected_member'],
          'date': q.date(date),
          'link': elem['link'],
          'text': [contrib['text']],
          'assembly': elem['assembly']
        }
        objects.append(object)
  for object in objects:
    client.query(q.create(
        q.collection(collection), {"data": object}
    ))

def loadJsonArrayFileToFaunaCollection(filepath, collection):
  rawFileData = open(filepath, 'r')
  jsonFileData = json.load(rawFileData)
  for elem in jsonFileData:
    client.query(q.create(
        q.collection(collection), {"data": elem}
    ))

def createFaunaIndex(name, collection, values=[], terms=[]):
  client.query(q.create_index({
    "name": name,
    "source": q.collection(collection),
    "values": values,
    "terms": terms,
  }))

def createFaunaFieldsArray(values):
  array = []
  for value in values:
    array.append({ 'field': ['data', value] })
  return array

# ### collection contributions ###
# client.query(q.create_collection({'name': 'contributions'}))
# filepath = '../senate_sessions.json'
# jsonTools.addFieldToJsonArrayFile(filepath, "assembly", "sénat")
# loadContributionsCollectionFromSessions('contributions', filepath)
# filepath = '../national_assembly_sessions.json'
# jsonTools.addFieldToJsonArrayFile(filepath, "assembly", "assemblée nationale")
# loadContributionsCollectionFromSessions('contributions', filepath)

# ### collection votes ###
# client.query(q.create_collection({"name": "votes"}))
# loadJsonArrayFileToFaunaCollection("../votes.json", "votes")

# ###  collection elected_members ###
# client.query(q.create_collection({"name":"elected_members"}))
# loadJsonArrayFileToFaunaCollection("../senators.json", "elected_members")
# loadJsonArrayFileToFaunaCollection("../deputies.json", "elected_members")

terms = []
values = []

# ### index for /elected_members ###
# values = createFaunaFieldsArray(['name', 'job', 'group', 'department'])
# createFaunaIndex('all_elected_members_name_job_group_department', 'elected_members', values)

# ### index for /elected_member ###
# values = [{'field': ['ref']}]
# terms = createFaunaFieldsArray(['name'])
# createFaunaIndex('elected_member_ref_by_name', 'elected_members', values, terms)
# terms = createFaunaFieldsArray(['elected_member'])
# createFaunaIndex('contributions_ref_by_elected_member', 'contributions', values, terms)

# ### indexes for /dates ###
# values = createFaunaFieldsArray(['date', 'link'])
# createFaunaIndex('contributions_date_link', 'contributions', values)

# ### indexes for /votes/context ###
# values = createFaunaFieldsArray(['date', 'assembly', 'number'])
# createFaunaIndex('votes_date_assembly_number', 'votes', values)

# ### indexes for /votes ###
# values = createFaunaFieldsArray(['vote_1'])
# terms = createFaunaFieldsArray(['job'])
# createFaunaIndex('elected_members_vote_1_by_job', 'elected_members', values, terms)

# values = createFaunaFieldsArray(['vote_2'])
# terms = createFaunaFieldsArray(['job'])
# createFaunaIndex('elected_members_vote_2_by_job', 'elected_members', values, terms)

# values = createFaunaFieldsArray(['vote_1'])
# terms = createFaunaFieldsArray(['job', 'group'])
# createFaunaIndex('elected_members_vote_1_by_job_group', 'elected_members', values, terms)

# values = createFaunaFieldsArray(['vote_2'])
# terms = createFaunaFieldsArray(['job', 'group'])
# createFaunaIndex('elected_members_vote_2_by_job_group', 'elected_members', values, terms)

### indexes for /visualization ####
values = createFaunaFieldsArray(['text'])
createFaunaIndex('all_contributions_text', 'contributions', values)

values = createFaunaFieldsArray(['name'])
terms = createFaunaFieldsArray(['group'])
createFaunaIndex('elected_members_name_by_group', 'elected_members', values, terms)

values = createFaunaFieldsArray(['text'])
terms = createFaunaFieldsArray(['assembly'])
createFaunaIndex('contributions_text_by_assembly', 'contributions', values, terms)

values = createFaunaFieldsArray(['text'])
terms = createFaunaFieldsArray(['elected_member'])
createFaunaIndex('contributions_text_by_elected_member', 'contributions', values, terms)

values = createFaunaFieldsArray(['text'])
terms = createFaunaFieldsArray(['elected_member', 'assembly'])
createFaunaIndex('contributions_text_by_elected_member_and_assembly', 'contributions', values, terms)