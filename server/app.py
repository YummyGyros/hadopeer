import os
import sys
from urllib.parse import urlparse
from faunadb import query as q
from faunadb.client import FaunaClient
from flask import (
  Flask, jsonify, request
)
from flask_cors import CORS

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

app = Flask(__name__)
CORS(app)

def getDataFaunaIndex(indexName, *args):
  if len(args) == 1:
    match = q.match(q.index(indexName), args[0])
  if len(args) == 2:
    match = q.match(q.index(indexName), args[0], args[1])
  return client.query(q.get(match))['data']

def paginateFaunaIndex(indexName, distinct = False, *args):
  if len(args) == 0:
    match = q.match(q.index(indexName))
  if len(args) == 1:
    match = q.match(q.index(indexName), args[0])
  if len(args) == 2:
    match = q.match(q.index(indexName), args[0], args[1])
  if distinct:
    match = q.distinct(match)
  return client.query(q.paginate(match))['data']

def countFaunaIndex(indexName, *args):
  if len(args) == 0:
    match = q.match(q.index(indexName))
  if len(args) == 1:
    match = q.match(q.index(indexName), args[0])
  if len(args) == 2:
    match = q.match(q.index(indexName), args[0], args[1])
  if len(args) == 3:
    match = q.match(q.index(indexName), args[0], args[1], args[2])
  return client.query(q.count(match))

@app.route("/")
def hello():
  # indexName = "a_group"
  # result = client.query(q.paginate(q.distinct(q.match(q.index(indexName)))))
  # print(result)
  return "hello"

### Elected Members ###
@app.route("/elected_members")
def elected_members():
  result = paginateFaunaIndex("all_elected_members_name_job_group_department")
  return jsonify(result)

### Elected Member ###
@app.route("/elected_member")
def elected_member():
  name = request.args.get('name')
  if not name:
    return "name not found", 400
  object = getDataFaunaIndex("elected_member_ref_by_name", name)
  return object

### Dates ###
@app.route("/dates")
def dates():
  dates_links = paginateFaunaIndex("all_dates_links")
  for elem in dates_links:
    elem[0] = elem[0].strftime("%d/%m/%Y")
  return jsonify(dates_links)

### Votes Context ###
@app.route("/votes/context")
def votes_context():
  return jsonify(paginateFaunaIndex("votes_date_assembly_number"))

### Votes ###
@app.route("/votes")
def votes():
  assembly = request.args.get("assembly")
  voteNumber = request.args.get("vote_number")
  group = request.args.get("group")
  job = "none"

  if not (assembly and voteNumber):
    return "400 Bad Request: assembly and vote_number are required", 400
  if not (voteNumber == "1" or voteNumber == "2"):
    return "400 Bad Request: vote_number is invalid: must be an int between 1 and maximum amount of votes", 400
  if assembly == "sénat":
    job = "sénateur"
  elif assembly == "assemblée nationale":
    job = "député"

  indexName = "elected_members_vote_" + voteNumber + "_by_vote_job"
  if group:
    indexName += "_group"
    inFavor = countFaunaIndex(indexName, "pour", job, group)
    against = countFaunaIndex(indexName, "contre", job, group)
    none = countFaunaIndex(indexName, "none", job, group)
    none += countFaunaIndex(indexName, "absent", job, group)
  else:
    inFavor = countFaunaIndex(indexName, "pour", job)
    against = countFaunaIndex(indexName, "contre", job)
    none = countFaunaIndex(indexName, "none", job)
    none += countFaunaIndex(indexName, "absent", job)
  return { "pour": inFavor, "contre": against, "none": none }

### Visualization ###
@app.route("/visualization")
def visualization():
  sample = request.args.get('sample')
  type = request.args.get('type')
  if not (type and sample):
    return "400 Bad Request: type required", 400
  return jsonify(getDataFaunaIndex('visualization_ref_by_type_sample', type, sample))

@app.route("/visualization/types")
def visualizations_types():
  return jsonify(paginateFaunaIndex("visualizations_type", True))

@app.route("/visualization/samples")
def visualizations_samples():
  return jsonify(paginateFaunaIndex("visualizations_sample", True))

### Others ###
@app.route("/political_groups")
def political_groups():
  return jsonify(paginateFaunaIndex("elected_members_group", True))