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

client.query(q.create_collection({"name":"politicians"}))
loadJsonArrayFileToFaunaCollection("../senators.json", "politicians")
loadJsonArrayFileToFaunaCollection("../deputies.json", "politicians")

client.query(q.create_collection({"name":"sessions"}))
addFieldToJsonArrayFile("../senate_sessions.json", "assembly", "senate")
addFieldToJsonArrayFile("../national_assembly_sessions.json", "assembly", "national_assembly")
loadJsonArrayFileToFaunaCollection("../senate_sessions.json", "sessions")
loadJsonArrayFileToFaunaCollection("../national_assembly_sessions.json", "sessions")