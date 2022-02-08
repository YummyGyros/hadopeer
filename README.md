# hadopeer

## Scrapping
run:
```shell
python3 .\hadopeer.py
```
setting:\
&emsp;`-pb ` :&emsp;add progress bar\
&emsp;`-noL` :&emsp;dont scrap lectures\
&emsp;`-pbS` :&emsp;dont scrap senator

## App

## Server
 
### FaunaDB

In order to start the server, access to our database with its key is required.

### Virtual Environment (venv)

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