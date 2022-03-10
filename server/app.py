import os
import json
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

@app.route("/")
def hello():
  return "hello"

@app.route("/participants")
def participants():
  # function = request.args.get('fonction')
  department = request.args.get('departement')
  politicalgroup = request.args.get('groupe_politique')

  # to refacto
  if department:
    if politicalgroup:
      toPaginate = q.union(
        q.match(q.index("senateurs_names_by_department_sorted_by_names"), department),
        q.match(q.index("senateurs_names_by_politicalgroup_sorted_by_names"), politicalgroup))
    else:
      toPaginate = q.union(q.match(q.index("senateurs_names_by_department_sorted_by_names"), department))
  elif politicalgroup:
    toPaginate = q.union(q.match(q.index("senateurs_names_by_politicalgroup_sorted_by_names"), politicalgroup))
  else:
    toPaginate = q.match(q.index("all_senateurs_values_sorted_by_names"))

  return jsonify(client.query(q.paginate(toPaginate))['data'])

@app.route("/participant")
def participant():
  name = request.args.get('name')
  if name:
    senateur_votes = client.query(q.paginate(q.match(q.index("senateur_values_by_name_sorted_by_names"), name)))['data']
    final = senateur_votes[0]
    final[-1] = [final[-1]]
    for i in range(1, len(senateur_votes)):
      final[-1].append(senateur_votes[i][-1])
    return jsonify(final)
  return "name not found", 400

@app.route("/dates")
def dates():
  return jsonify(client.query(q.paginate(q.match(
    q.index("seances_with_date_link")
  )))['data'])

@app.route("/votes/context")
def votes_context():
  array = client.query(q.paginate(q.match(
    q.index("seances_senat_with_date_link")
  )))['data']
  for elem in array:
    elem[1] = "Sénat"
  # implem deputes
  # array = client.query(q.paginate(q.match(
  #   q.index("seances_AN_with_date_link")
  # )))['data']
  # for elem in array:
  #   elem[1] = "Assemblée Nationale"
  return jsonify(array)

@app.route("/votes")
def votes():
  assemblee = request.args.get("assemblee")
  number = request.args.get("number")
  politicalgroup = request.args.get("groupe_politique")
  if not (assemblee and number):
    return "bad request: assemblee and number are required", 500

  voteNumber = int(number)
  if voteNumber < 1:
    return "bad request: invalid vote number, below one", 500

  if assemblee == "Sénat":
    seancesSenat = client.query(q.paginate(q.match(
      q.index("seances_senat_with_date_link")
    )))['data']
    totalVotesSenat = len(seancesSenat)
    if voteNumber > totalVotesSenat:
      return "bad request: invalid vote number, too big", 500
    voteNumber -= 1

    if politicalgroup:
      match = q.match(q.index("senateurs_scrutins_by_politicalgroup"), politicalgroup)
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
    # elif assemblee == "Assemblée nationale":
    #   if politicalgroup:
    #     match = q.match(q.index("deputes_scrutins_by_politicalgroup"), politicalgroup)
      # else:
      #   match = q.match(q.index("deputes_scrutins"), politicalgroup)