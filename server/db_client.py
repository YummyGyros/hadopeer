

# Import the driver, and other required packages
import os
import sys
from urllib.parse import urlparse
from faunadb import query as q
from faunadb.client import FaunaClient

# Acquire the secret and optional endpoint from environment variables
secret = os.getenv("FAUNADB_SECRET")
endpoint = os.getenv("FAUNADB_ENDPOINT")

if not secret:
  print("The FAUNADB_SECRET environment variable is not set, exiting.")
  sys.exit(1)

endpoint = endpoint or "https://db.fauna.com/"

o = urlparse(endpoint)

# Instantiate a client
client = FaunaClient(
  secret=secret,
  domain=o.hostname,
  port=o.port,
  scheme=o.scheme
)

# Create a collection called 'myCollection'
result = client.query(
  q.create_collection({"name": "myCollection"})
)

# Show the result
print(result)