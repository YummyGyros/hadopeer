import os
import sys
from tkinter.font import names
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


@app.route("/elected_member")
def elected_member():
  name = request.args.get('name')
  if not name:
    return "name not found", 400
  object = getDataFaunaIndex("elected_member_ref_by_name", name)
  object['contributions'] = getDataFaunaIndex("contributions_ref_by_elected_member", name)
  return object


@app.route("/dates")
def dates():
  return jsonify(paginateFaunaIndex("contributions_date_link"))


@app.route("/votes/context")
def votes_context():
  return jsonify(paginateFaunaIndex("votes_date_assembly_number"))


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


@app.route("/visualization")
def visualization():
  assembly = request.args.get('assembly')
  group = request.args.get('group')
  type = request.args.get('type')

  if group:
    contribs = []
    names = paginateFaunaIndex("elected_members_name_by_group", group)
    if assembly:
      for name in names:
        tmpObjects = paginateFaunaIndex("contributions_text_by_elected_member_and_assembly", name, assembly)
        for tmpObject in tmpObjects:
          contribs.append(tmpObject)
    else:
      for name in names:
        tmpObjects = paginateFaunaIndex("contributions_text_by_elected_member", name)
        for tmpObject in tmpObjects:
          contribs.append(tmpObject)
    return jsonify(contribs)
  
  if assembly:
    return jsonify(paginateFaunaIndex("contributions_text_by_assembly", assembly))
  else:
    return jsonify(paginateFaunaIndex("all_contributions_text"))
  # launch nlp function depending on type var