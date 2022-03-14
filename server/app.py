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
  function = request.args.get('function')
  group = request.args.get('group')
  department = request.args.get('department')
  result = client.query(q.paginate(q.match(
    q.index("all_elected_members_name_function_group_department")
  )))['data']
  if function:
    result = [values for values in result if values[1] == function]
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


# issue ongoing:
#   indexes count for one when values are identical in array 'scrutins'
@app.route("/votes")
def votes():
  assembly = request.args.get("assembly")
  voteNumber = request.args.get("vote_number")
  group = request.args.get("group")
  function = "none"

  if not (assembly and voteNumber):
    return "bad request: assembly and vote_number are required", 400
  if assembly == "sénat":
    function = "sénateur"
  elif assembly == "assemblée nationale":
    function = "député"

  try:
    voteNumber = int(voteNumber)
  except:
    return "bad request: invalid vote_number, is not an integer"
  if voteNumber < 1:
    return "bad request: invalid vote_number, below one", 400
  sessions = client.query(q.paginate(q.match(
    q.index("sessions_date_assembly")
  )))['data']
  totalVotes = 0
  for session in sessions:
    if session[1] == assembly:
      totalVotes += 1
  if voteNumber > totalVotes:
    return "bad request: invalid vote number, too big", 400
  voteNumber -= 1
  print("number:", voteNumber)

  if group:
    match = q.union(
      q.match(q.index("elected_members_scrutins_by_function"), function),
      q.match(q.index("elected_members_scrutins_by_group"), group)
    )
  else:
    match = q.match(q.index("elected_members_scrutins_by_function"), function)
  allScrutins = client.query(q.paginate(match))['data']
  print("allScrutins: ", allScrutins)

  selectedScrutins = []
  while (voteNumber < len(allScrutins)):
    selectedScrutins.append(allScrutins[voteNumber])
    voteNumber += totalVotes
  print("selectedScrutins: ", selectedScrutins)
  return { "pour": selectedScrutins.count("pour"),
            "contre": selectedScrutins.count("contre"),
            "none": selectedScrutins.count("none") + selectedScrutins.count("absent")}


# refacto AN
@app.route("/visualization")
def visualization():
  group = request.args.get('group')
  assembly = request.args.get('assembly')
  result = "none"

  if group:
    result = client.query(q.paginate(q.match(q.index("elected_members_paroles_by_group"), group)))['data']
  else:
    result = client.query(q.paginate(q.match(q.index("all_elected_members_paroles"))))['data']
  # need interventions with elected member data
  # filter depending on assembly
  if result == "none":
    return "name not found", 400
  return jsonify(result)