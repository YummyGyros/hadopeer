import os
import sys
import json
from urllib.parse import urlparse
from faunadb import query as q
from faunadb.client import FaunaClient

def getFaunaDbInstance():
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
    return client

def loadJsonArrayFileToFaunaCollection(client, filepath, collection):
  rawFileData = open(filepath, 'r')
  jsonFileData = json.load(rawFileData)
  for elem in jsonFileData:
    client.query(q.create(
        q.collection(collection), {"data": elem}
    ))

def createFaunaFieldsArray(values):
  array = []
  for value in values:
    array.append({ 'field': ['data', value] })
  return array