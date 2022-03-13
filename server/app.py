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

# refacto AN
@app.route("/votes")
def votes():
  assemblee = request.args.get("assemblee")
  number = request.args.get("number")
  group = request.args.get("groupe_politique")
  if not (assemblee and number):
    return "bad request: assemblee and number are required", 400
  voteNumber = int(number)
  if voteNumber < 1:
    return "bad request: invalid vote number, below one", 400

  if assemblee == "Sénat":
    seancesSenat = client.query(q.paginate(q.match(
      q.index("seances_senat_with_date_link")
    )))['data']
    totalVotesSenat = len(seancesSenat)
    if voteNumber > totalVotesSenat:
      return "bad request: invalid vote number, too big", 400
    voteNumber -= 1
    if group:
      match = q.match(q.index("senateurs_scrutins_by_group"), group)
    else:
      match = q.match(q.index("senateurs_scrutins"))
    allScrutins = client.query(q.paginate(match))['data']

    selectedScrutins = []
    while (voteNumber < len(allScrutins)):
      selectedScrutins.append(allScrutins[voteNumber])
      voteNumber += totalVotesSenat
    return { "pour": selectedScrutins.count("pour"),
              "contre": selectedScrutins.count("contre"),
              "none": selectedScrutins.count("none") + selectedScrutins.count("absent")}
    # duplicate all for AN
    # duplicate indexes too

# refacto AN
@app.route("/visualization")
def visualisation():
  group = request.args.get('group')
  assembly = request.args.get('assembly')
  result = "none"

  if group:
    result = client.query(q.paginate(q.match(q.index("elected_members_paroles_by_group"), group)))['data']
  else:
    result = client.query(q.paginate(q.match(q.index("all_elected_members_paroles"))))['data']
  # filter depending on assembly
  if result == "none":
    return "name not found", 400
  return jsonify(result)