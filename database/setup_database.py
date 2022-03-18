import os
import json
import sys
from urllib.parse import urlparse
from faunadb import query as q
from faunadb.client import FaunaClient

import jsonTools

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

def addInterventionsFromSessionsToElectedMembers(sessionsPath, membersPath):
  jsonTools.addFieldToJsonArrayFile(membersPath, "contributions", [])
  rawFileData = open(sessionsPath, 'r')
  sessions = json.load(rawFileData)
  for session in sessions:
    for article in session['articles']:
      for contribution in article['contributions']:
        jsonTools.addValueToArrayInObjectOfJsonArrayFile(
          membersPath,
          "name", contribution['elected_member'],
          "contributions", contribution['text']
        )

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

# extract contributions from sessions files to elected_members files ###
addInterventionsFromSessionsToElectedMembers("../senate_sessions.json", "../senators.json")
jsonTools.deleteFieldFromJsonArrayFile("../senate_sessions.json", "articles")
addInterventionsFromSessionsToElectedMembers("../national_assembly_sessions.json", "../deputies.json")
jsonTools.deleteFieldFromJsonArrayFile("../national_assembly_sessions.json", "articles")

###  collection elected_members ###
client.query(q.create_collection({"name":"elected_members"}))
loadJsonArrayFileToFaunaCollection("../senators.json", "elected_members")
loadJsonArrayFileToFaunaCollection("../deputies.json", "elected_members")

### collection sessions ###
client.query(q.create_collection({"name":"sessions"}))
jsonTools.addFieldToJsonArrayFile("../senate_sessions.json", "assembly", "sénat")
jsonTools.addFieldToJsonArrayFile("../national_assembly_sessions.json", "assembly", "assemblée nationale")
loadJsonArrayFileToFaunaCollection("../senate_sessions.json", "sessions")
loadJsonArrayFileToFaunaCollection("../national_assembly_sessions.json", "sessions")

terms = []
values = []

### index for /elected_members ###
values = createFaunaFieldsArray(['name', 'job', 'group', 'department'])
createFaunaIndex('all_elected_members_name_job_group_department', 'elected_members', values)

### index for /elected_member ###
values = [{'field': ['ref']}]
terms = createFaunaFieldsArray(['name'])
createFaunaIndex('elected_member_ref_by_name', 'elected_members', values, terms)

### indexes for /dates ###
values = createFaunaFieldsArray(['date', 'link'])
createFaunaIndex('sessions_date_link', 'sessions', values)

values = createFaunaFieldsArray(['date', 'assembly'])
createFaunaIndex('sessions_date_assembly', 'sessions', values)

### indexes for /votes ###
values = createFaunaFieldsArray(['vote_1'])
terms = createFaunaFieldsArray(['job'])
createFaunaIndex('elected_members_vote_1_by_job', 'elected_members', values, terms)

values = createFaunaFieldsArray(['vote_2'])
terms = createFaunaFieldsArray(['job'])
createFaunaIndex('elected_members_vote_2_by_job', 'elected_members', values, terms)

values = createFaunaFieldsArray(['vote_1'])
terms = createFaunaFieldsArray(['job', 'group'])
createFaunaIndex('elected_members_vote_1_by_job_group', 'elected_members', values, terms)

values = createFaunaFieldsArray(['vote_2'])
terms = createFaunaFieldsArray(['job', 'group'])
createFaunaIndex('elected_members_vote_2_by_job_group', 'elected_members', values, terms)

### indexes for /visualization ####
values = createFaunaFieldsArray(['contributions'])
createFaunaIndex('all_elected_members_contributions', 'elected_members', values)

values = createFaunaFieldsArray(['contributions'])
terms = createFaunaFieldsArray(['group'])
createFaunaIndex('elected_members_contributions_by_group', 'elected_members', values, terms)

values = createFaunaFieldsArray(['contributions'])
terms = createFaunaFieldsArray(['job'])
createFaunaIndex('elected_members_contributions_by_job', 'elected_members', values, terms)

values = createFaunaFieldsArray(['contributions'])
terms = createFaunaFieldsArray(['job', 'group'])
createFaunaIndex('elected_members_contributions_by_job_group', 'elected_members', values, terms)