#!/usr/bin/python

import click
import requests 
import json

SERVICE_URL = "http://localhost:8000"
@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', prompt=True)
@click.option('--accuracy', prompt=True)
@click.option('--owner', prompt=True)
@click.option('--feature_names', prompt=True)
@click.option('--hyperparameters', prompt=True)
@click.option('--train_start', prompt=True)
@click.option('--train_stop', prompt=True)
def create_model(name, accuracy, owner, feature_names, hyperparameters, train_start, train_stop):
    payload = {
    	'name': name,
    	'accuracy': float(accuracy),
    	'owner': owner,
    	'feature_names': eval(feature_names),
    	'hyperparameters': eval(hyperparameters), 
    	'train_start': int(train_start),
    	'train_stop': int(train_stop)
    }
    print json.dumps(payload)
    resp = requests.post(SERVICE_URL + "/models/", json=payload)
    print resp.text

@cli.command()
@click.option('--id', prompt=True)
def get_model(id):
    resp = requests.get(SERVICE_URL + "/models/{}".format(id))
    print resp.text

@cli.command()
@click.option('--id', prompt=True)
def delete_model(id):
    resp = requests.delete(SERVICE_URL + "/models/{}".format(id))
    print resp.text

@cli.command()
@click.option('--owner', prompt=True)
def most_recent(owner):
    resp = requests.get(SERVICE_URL + "/models/{}/most-recent".format(owner))
    print resp.text

@cli.command()
@click.option('--owner', prompt=True)
def most_accurate(owner):
    resp = requests.get(SERVICE_URL + "/models/{}/most-accurate".format(owner))
    print resp.text

if __name__ == '__main__':
	cli()