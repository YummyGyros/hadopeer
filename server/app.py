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

@app.route("/participants")
def participants():
  function = request.args.get('fonction')
  group = request.args.get('groupe')
  department = request.args.get('département')
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

@app.route("/participant")
def participant():
  name = request.args.get('name')
  if name:
    senateurValues = client.query(q.get(q.match(q.index("senateur_ref_by_name"), name)))['data']
    return jsonify(senateurValues)
  return "name not found", 400

@app.route("/dates")
def dates():
  return jsonify(client.query(q.paginate(q.match(
    q.index("seances_with_date_link")
  )))['data'])

# refacto AN
# add index getting "date" & "assemblee" field
@app.route("/votes/context")
def votes_context():
  array = client.query(q.paginate(q.match(
    q.index("seances_with_date_link")
  )))['data']
  for elem in array:
    elem[1] = "Sénat"
  return jsonify(array)

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
@app.route("/visualisation")
def visualisation():
  group = request.args.get('groupe_politique')
  assembly = request.args.get('assemblee')
  senateurValues = "none"
  if assembly:
    if group:
      senateurValues = client.query(q.paginate(q.match(q.index("senateurs_paroles_by_group"), group)))['data']
    else:
      senateurValues = client.query(q.paginate(q.match(q.index("all_senateurs_paroles"))))['data']
  # deputies
  # else:
    # senateur + deputies
  if senateurValues == "none":
    return "name not found", 400
  return jsonify(senateurValues)