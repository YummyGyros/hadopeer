# hadopeer

Python Version: 3.8.10

## Table of content

  - [Introduction](#introduction)
  - [Virtual Environments](#virtual-environments)
  - [Scrapping](#scrapping)
  - [Database](#database)
  - [Server](#server)
  - [App](#app)
  - [About us](#about-us)

## Introduction

This project is from Epitech LabResearch.<br>
Its goal is to present analyzed debates data from France's senate and national assembly around Hadopi.<br>

First, data's scrapped from the official public websites. <br>
Then, we create a Fauna database that the Flask server will make requests to.<br>
Before that a React frontend makes request to this REST API, NLP is done in the server to analyze the data.<br>

And there we have a functionnal website, ready for production, allowing us to share the results of our analysis.<br>

It is the Proof Of Concept of a project of a larger scale, that could analyze all debates on any law project.<br>

## Virtual Environments

This project uses python virtual environments in order to manage dependencies neatly.<br>
To launch python scripts, you will need to activate the venv so it can use its dependencies.<br>
When you're done you need to deactivate it.

Here are the commands:
```
source .venv/bin/activate
[execute commands here]
deactivate
```

## Scrapping
run:
```shell
python3 ./scrapping/hadopeer.py
```
setting:\
&emsp;`-pb` :&emsp; progress bar\
&emsp;`-noL` :&emsp; not scrapping sessions\
&emsp;`-noS` :&emsp; not scrapping elected members

## Database

FaunaDB is the database we've chosen. It is a multi-model database, which makes it very flexible and very efficient at the same time.<br>
If you want to start the database, you have to get an account, create a database and retrieve its secret key.
https://docs.fauna.com/fauna/current/<br>


In the database folder, you will find the files that take care of creating the database from the scrapping json files.<br>
Launch the command to set it up:
```
FAUNADB_SECRET=your_secret python3 setup_database.py
```

## Server

In order to start the server, access to our database with its secret key is required.<br>
You will need to have launched our database setup script successfully beforehand too.

```
FAUNADB_SECRET=your_secret flask run
```

## App

insert text on app here

## About us

This initiative of this project is from Epitech LabResearch's historian Marie Puren.<br>
It has been developped by three students from Epitech Paris:
- [Adrien Mallet](https://github.com/jack-a-dit)
- [Mattéo Theboul](https://github.com/MTheboul)
- [Robin Levavasseur](https://github.com/YummyGyros)