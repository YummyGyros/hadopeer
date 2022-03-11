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

# one or two collections?
# Publish a document for each person in the "senateurs_only" collection
senateursFile = open('../senateurs.json', 'r')
db = json.load(senateursFile)
client.query(q.create_collection({"name":"senateurs"}))
for elu in db:
    client.query(q.create(
        q.collection("senateurs"), {"data": elu}
    ))

# Publish a document for each lecture in the "seances" collection (from both senate and AN files)
lecturesSenatFile = open('../db_testlectures.json', 'r')
lecturesSenat = json.load(lecturesSenatFile)
client.query(q.create_collection({"name":"seances"}))
for lecture in lecturesSenat['lectures_senat']:
    client.query(q.create(
        q.collection("seances"), {"data": lecture}
    ))