import os
import sys
from urllib.parse import urlparse
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