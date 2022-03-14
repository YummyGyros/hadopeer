import os
import json
import sys
from urllib.parse import urlparse
from faunadb import query as q
from faunadb.client import FaunaClient

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

def loadJsonArrayFileToFaunaCollection(filepath, collection):
  rawFileData = open(filepath, 'r')
  jsonFileData = json.load(rawFileData)
  for elem in jsonFileData:
    client.query(q.create(
        q.collection(collection), {"data": elem}
    ))

def addFieldToJsonArrayFile(filepath, field, value):
  dataString = open(filepath, 'r')
  objects = json.load(dataString)
  for object in objects:
    object[field] = value
  with open(filepath, "w") as file:
    json.dump(objects, file, ensure_ascii=True, indent=4, separators=(',', ': '))

def addValueToArrayInObjectOfJsonArrayFile(filepath, fieldObj, valueObj, field, value):
  file = open(filepath, 'r')
  objects = json.load(file)
  for object in objects:
    if object[fieldObj] == valueObj.lower():
      object[field].append(value)
      break
  with open(filepath, "w") as file:
    json.dump(objects, file, ensure_ascii=True, indent=4, separators=(',', ': '))

def addInterventionsFromSessionsToElectedMembers(sessionsPath, membersPath):
  addFieldToJsonArrayFile(membersPath, "contributions", [])
  rawFileData = open(sessionsPath, 'r')
  sessions = json.load(rawFileData)
  for session in sessions:
    for article in session['articles']:
      for intervention in article['interventions']:
        addValueToArrayInObjectOfJsonArrayFile(
          membersPath,
          "nom", intervention['orateur_nom'],
          "contributions", intervention['texte']
        )

##### add interventions from sessions files to elected_members files #####
addInterventionsFromSessionsToElectedMembers("../senate_sessions.json", "senators.json")
addInterventionsFromSessionsToElectedMembers("../national_assembly_sessions.json", "deputiess.json") 

##### collection elected_members #####
client.query(q.create_collection({"name":"elected_members"}))
loadJsonArrayFileToFaunaCollection("../senators.json", "elected_members")
loadJsonArrayFileToFaunaCollection("../deputies.json", "elected_members")

##### collection sessions #####
client.query(q.create_collection({"name":"sessions"}))
addFieldToJsonArrayFile("../senate_sessions.json", "assemblée", "sénat")
addFieldToJsonArrayFile("../national_assembly_sessions.json", "assemblée", "assemblée nationale")
loadJsonArrayFileToFaunaCollection("../senate_sessions.json", "sessions")
loadJsonArrayFileToFaunaCollection("../national_assembly_sessions.json", "sessions")