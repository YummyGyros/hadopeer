import os
import json
import sys
import re
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

@app.route("/")
def hello():
  return "hello"

# To reduce calls to Fauna we filter the array in python directly.
# It is possible because our filters corresponds to the values displayed.
# otherwise with Fauna:
#   res = paginate
#   res = filter_(lambda x: q.equals(x, "hello"), res)
#   client.query(res)['data]
@app.route("/elected_members")
def elected_members():
  job = request.args.get('job')
  group = request.args.get('group')
  department = request.args.get('department')
  result = client.query(q.paginate(q.match(
    q.index("all_elected_members_name_job_group_department")
  )))['data']
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
  if name:
    senateurValues = client.query(q.get(q.match(q.index("elected_member_ref_by_name"), name)))['data']
    return jsonify(senateurValues)
  return "name not found", 400


@app.route("/dates")
def dates():
  return jsonify(client.query(q.paginate(q.match(
    q.index("sessions_date_link")
  )))['data'])


@app.route("/votes/context")
def votes_context():
  return jsonify(client.query(q.paginate(q.match(
    q.index("sessions_date_assembly")
  )))['data'])


# fixes:
#   - get total and create all necessary indexes at init
#   - error handling voteNumber
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
    match = q.match(q.index(indexName + "_by_job_group"), job, group)
  else:
    match = q.match(q.index(indexName + "_by_job"), job)
  votes = client.query(q.paginate(match))['data']
  print("votes: ", votes)
  return { "pour": votes.count("pour"),
            "contre": votes.count("contre"),
            "none": votes.count("none") + votes.count("absent")}


@app.route("/visualization")
def visualization():
  assembly = request.args.get('assembly')
  group = request.args.get('group')
  type = request.args.get('type')
  job = ""
  if not type:
    return "bad request: type is required", 400
  if assembly == "sénat":
    job = "sénateur"
  elif assembly == "assemblée nationale":
    job = "député"

  if assembly:
    if group:
      match = q.match(q.index("elected_members_contributions_by_job_group"), job, group,)
    else:
      match = q.match(q.index("elected_members_contributions_by_job"), job)
  elif group:
    match = q.match(q.index("elected_members_contributions_by_group"), group)
  else:
    print('else')
    match = q.match(q.index("all_elected_members_contributions"))
  return jsonify(client.query(q.paginate(match))['data'])