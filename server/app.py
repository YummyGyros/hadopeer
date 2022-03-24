import os
import sys
from urllib.parse import urlparse
from faunadb import query as q
from faunadb.client import FaunaClient
from flask import (
  Flask, jsonify, request
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

app = Flask(__name__)

def getDataFaunaIndex(indexName, arg):
  match = q.match(q.index(indexName), arg)
  return client.query(q.get(match))['data']

def paginateFaunaIndex(indexName, *args):
  if len(args) == 0:
    match = q.match(q.index(indexName))
  if len(args) == 1:
    match = q.match(q.index(indexName), args[0])
  if len(args) == 2:
    match = q.match(q.index(indexName), args[0], args[1])
  return client.query(q.paginate(match))['data']


@app.route("/")
def hello():
  return "hello"

### Elected Members ###
@app.route("/elected_members")
def elected_members():
  job = request.args.get('job')
  group = request.args.get('group')
  department = request.args.get('department')

  result = paginateFaunaIndex("all_elected_members_name_job_group_department")
  if job:
    result = [values for values in result if values[1] == job]
  if group:
    result = [values for values in result if values[2] == group]
  if department:
    result = [values for values in result if values[3] == department]
  return jsonify(result)

### Elected Member ###
@app.route("/elected_member")
def elected_member():
  return "Error 500: Internal error. Endpoint to be implemented soon.", 500
  # name = request.args.get('name')
  # if not name:
  #   return "name not found", 400
  # object = getDataFaunaIndex("elected_member_ref_by_name", name)
  # object['contributions'] = getDataFaunaIndex("contributions_ref_by_elected_member", name)
  # return object

### Dates ###
def isContainedInArray(object, array):
  for elem in array:
    save = True
    if len(object) != len(elem):
      continue
    for i in range(len(object)):
      if object[i] != elem[i]:
        save = False
      if not save:
        continue
    if save:
      return True
  return False

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
    return "bad request: assembly and vote_number are required", 400
  if not (voteNumber == "1" or voteNumber == "2"):
    return "bad request: vote_number is invalid: must be an int between 1 and maximum amount of votes"
  if assembly == "sénat":
    job = "sénateur"
  elif assembly == "assemblée nationale":
    job = "député"

  indexName = "elected_members_vote_" + voteNumber
  if group:
    votes = paginateFaunaIndex(indexName + "_by_job_group", job, group)
  else:
    votes = paginateFaunaIndex(indexName + "_by_job", job)
  return { "pour": votes.count("pour"),
            "contre": votes.count("contre"),
            "none": votes.count("none") + votes.count("absent")}

### Visualization ###
def extractDataFromNamesToArray(objects, names, index, *args):
  for name in names:
    if len(args) == 1:
      tmpObjects = paginateFaunaIndex(index, name, args[0])
    else:
      tmpObjects = paginateFaunaIndex(index, name)
    for tmpObject in tmpObjects:
      objects.append(tmpObject)

@app.route("/visualization")
def visualization():
  assembly = request.args.get('assembly')
  group = request.args.get('group')
  type = request.args.get('type')

  if group:
    contribs = []
    names = paginateFaunaIndex("elected_members_name_by_group", group)
    if assembly:
      extractDataFromNamesToArray(contribs, names, "contributions_text_by_elected_member_and_assembly", assembly)
    else:
      extractDataFromNamesToArray(contribs, names, "contributions_text_by_elected_member")
  elif assembly:
    contribs = paginateFaunaIndex("contributions_text_by_assembly", assembly)
  else:
    contribs = paginateFaunaIndex("all_contributions_text")
  # NLP: use contribs and type
  return jsonify(contribs)

### Others ###
@app.route("/political_groups")
def political_groups():
  return jsonify(paginateFaunaIndex("elected_members_group"))