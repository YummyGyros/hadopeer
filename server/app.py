
from flask import (
    Flask, jsonify
)
from faunadb import query as q
from hadopeer.server.faunadb import client

app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify(client.query(
        q.get(q.ref(q.collection("myCollection"), "322765143676027468"))
    )["data"])