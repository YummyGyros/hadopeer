# hadopeer

## Scrapping
run:
```shell
python3 ./scrapping/hadopeer.py
```
setting:\
&emsp;`-pb ` :&emsp;add progress bar\
&emsp;`-noL` :&emsp;don't scrap lectures\
&emsp;`-pbS` :&emsp;don't scrap senators

## App

insert text on app here

## Database

DO NOT USE FILES AT THE MOMENT. 
They re only records of what's been done but aren't ready-to-use.

Fauna is the database we've chosen. It is a multi-model database, which makes it very flexible but still very efficient.
In the corresponding folder, you will find the files that take care of creating the database from the scrapping json files.

TMP: these are in fql at the moment. It will then be transformed in a full python script (including creation of collection from files).

## Server
 
### Database warning

In order to start the server, access to our database with its secret key is required.

### Virtual Environment (venv)

It is required to use virtual environments to use the server.\
Activate/Deactivate the server's virtual environment:

```shell
source server_env/bin/activate
```

To exit the venv:
```shell
deactivate
```

### Run

```shell
flask run
```