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

Fauna is the database we've chosen. It is a multi-model database, which makes it very flexible but still very efficient.
In the corresponding folder, you will find the files that take care of creating the database from the scrapping json files.

```
source .venv/bin/activate
FAUNADB_SECRET=your_secret python3 setup_database.py
deactivate
```

## Server
 
### Database warning

In order to start the server, access to our database with its secret key is required.
You will need to have launched our database setup script successfully beforehand too.

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

```
FAUNADB_SECRET=your_secret flask run
```