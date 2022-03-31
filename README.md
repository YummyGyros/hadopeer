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

This project is from Epitech's LabResearch.\
Its goal is to present analyzed debates data from France's senate and national assembly around Hadopi.\
It is the Proof Of Concept for a large scale project that could analyze all debates on any french law project.\

Here's the process of the project:
- Data scrapping from the official websites of the senate and the national assembly
- Natural Language Processing (NLP) with the data to produce visualizations
- Useful data stored into a Fauna Database (cloud)
- The Python Flask REST API requests data to serve it on particular endpoints (see /server/RESTAPI.md)
- A frontend in React presenting the data

The server and website were sent to production through Vercel.

## Virtual Environments

In the python folders, you will find a "requirements.txt" file.\
This file lists all required packages with their version to make the code work.\
It is perfect for virtual environments use and prevents from dependecies issues!

Create the venv:
```
python3 -m venv .venv
```

Activate it:
```
source .venv/bin/activate
```

Install the packages:
```
pip install -r requirements.txt
```

Execute your commands here and then:
```
deactivate
```

The database-setup has a special step which is why there's a script for it.

## Scrapping

Data is scrapped into 5 json files from the following websites:
- https://www.assemblee-nationale.fr/13/dossiers/internet.asp
- http://www.senat.fr/dossier-legislatif/pjl07-405.html

```
python3 ./scrapping/hadopeer.py
```

setting:\
&emsp;`-pb` :&emsp; progress bar\
&emsp;`-noL` :&emsp; not scrapping sessions\
&emsp;`-noS` :&emsp; not scrapping elected members

## Database

FaunaDB is the database we've chosen. It is a multi-model database, which makes it very flexible and very efficient at the same time.\
If you want to start the database, you have to get an account, create a database and retrieve its **secret key**.\
https://docs.fauna.com/fauna/current/ \

To make things simpler, we created a script so you can set up everything easily.\
However, you will need to **complete** it with your fauna secret key.\

Once done:
```
./database-setup/init_db.sh
```

N.B.: Creating all visualizations for one NLP analysis takes around 10mn. If you take the senate only it should be around 1mn.

## Server

In order to start the server and access a database, a secret key is required.\
To do so, see previous section.

If you're ready:
```
cd server
FAUNADB_SECRET=your_secret flask run
```

## App

We developped a basic React front end, to start it locally:
```
npm start
``

## About us

This project has been initiated by Epitech LabResearch's historian Marie Puren.\
It has been developped by three students from Epitech Paris:
- [Adrien Mallet](https://github.com/jack-a-dit)
- [Mattéo Theboul](https://github.com/MTheboul)
- [Robin Levavasseur](https://github.com/YummyGyros)
