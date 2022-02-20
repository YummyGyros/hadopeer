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

## Server
 
### FaunaDB

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