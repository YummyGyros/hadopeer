from flask import Flask

app = Flask(__name__)

@app.route("/")
def welcome():
    return "Bienvenue sur la page d'accueil!"

@app.route("/votes")
def votes():
    return "Visualisation de votes"

@app.route("/participants")
def participants():
    return "Liste des participants"

@app.route("/analyse")
def analyse():
    return "Analyse des discours avec visuels"

@app.route("/chronologie")
def chronologie():
    return "Frise chronologique du projet de lois"