from boto3.dynamodb.conditions import Key, Attr
from decimal import *

from flask import Flask
from flask import jsonify, request, abort, redirect
from flask_dynamo import Dynamo

import hashlib
import simplejson as json

app = Flask(__name__)

app.config['DYNAMO_TABLES'] = [{
    'TableName':
    'models',
    # Need secondary indexes with range keys
    # so I need to define one here...
    'KeySchema': [
        dict(AttributeName='id', KeyType='HASH'),
        dict(AttributeName='owner', KeyType='RANGE'),
    ],
    'GlobalSecondaryIndexes': [
        # used to calculate most_recent
        {
            'IndexName':
            'models_train_stop',
            'KeySchema': [
                dict(AttributeName='owner', KeyType='HASH'),
                dict(AttributeName='train_stop', KeyType='RANGE')
            ],
            'Projection':
            dict(ProjectionType='ALL'),
            'ProvisionedThroughput':
            dict(ReadCapacityUnits=1, WriteCapacityUnits=1)
        },
        # used to calculate most_accurate
        {
            'IndexName':
            'models_accuracy',
            'KeySchema': [
                dict(AttributeName='owner', KeyType='HASH'),
                dict(AttributeName='accuracy', KeyType='RANGE')
            ],
            'Projection':
            dict(ProjectionType='ALL'),
            'ProvisionedThroughput':
            dict(ReadCapacityUnits=1, WriteCapacityUnits=1)
        },
        # used to query with only "id"
        {
            'IndexName':
            'models_id',
            'KeySchema': [
                dict(AttributeName='id', KeyType='HASH'),
            ],
            'Projection':
            dict(ProjectionType='ALL'),
            'ProvisionedThroughput':
            dict(ReadCapacityUnits=1, WriteCapacityUnits=1)
        },
    ],
    'AttributeDefinitions': [
        # owner of model
        dict(AttributeName='id', AttributeType='S'),
        # owner of model
        dict(AttributeName='owner', AttributeType='S'),
        # decimal representing accuracy of model
        dict(AttributeName='accuracy', AttributeType='N'),
        #Timestamp in Unix Epoch
        dict(AttributeName='train_stop', AttributeType='N')
    ],
    'ProvisionedThroughput':
    dict(ReadCapacityUnits=2, WriteCapacityUnits=2)
}]
dynamo = Dynamo(app)

table = dynamo.tables['models']

# Create a Model object in DynamoDB
@app.route('/models/', methods=["POST"])
def create_model():
    # Doing no validation, super dirty
    data = request.get_json(silent=True)
    print(data)
    data = {
        "name": data.get('name', None),
        # this is madness...: https://github.com/boto/boto3/issues/665
        "accuracy": Decimal(str(data.get('accuracy', None))),
        "owner": data.get('owner', None),
        "feature_names": data.get('feature_names', None),
        "hyperparameters": data.get('hyperparameters', None),
        "train_start": data.get('train_start', None),
        "train_stop": data.get('train_stop', None)
    }
    # ID is hash of dict contents to prevent duplicates
    m = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8'))
    data["id"] = m.hexdigest()
    item = table.put_item(Item=data)
    return json.dumps(data)

# Get an existing model in DynamoDB 
@app.route('/models/<id>', methods=["GET"])
def get_model(id):
    response = table.query(
        IndexName="models_id",
        Select="ALL_PROJECTED_ATTRIBUTES",
        ScanIndexForward=False,
        KeyConditionExpression=Key('id').eq(id),
    )
    item = response["Items"][0]
    if item:
        return json.dumps(item)

# Delete an existing model in DynamoDB
@app.route('/models/<id>', methods=["DELETE"])
def delete_model(id):
    # make a query to the ID-only index first
    response = table.query(
        IndexName="models_id",
        Select="ALL_PROJECTED_ATTRIBUTES",
        ScanIndexForward=False,
        KeyConditionExpression=Key('id').eq(id),
    )
    # Get the item fromt the query
    item = response["Items"][0]
    # and use its data to delete from the base-table
    key = {"id": item["id"], "owner": item["owner"]}
    delete_response = table.delete_item(Key=key)
    return json.dumps({"deleted": True})

# Get the most-recently trained model by owner
@app.route('/models/<owner>/most-recent', methods=["GET"])
def get_most_recent(owner):
    # query the train_stop index and scan index by train_stops
    response = table.query(
        IndexName="models_train_stop",
        Select="ALL_PROJECTED_ATTRIBUTES",
        ScanIndexForward=False,
        KeyConditionExpression=Key('owner').eq(owner),
    )
    latest = response["Items"][0]
    if latest:
        return json.dumps(latest)

# Get most-accurate model by owner
@app.route('/models/<owner>/most-accurate', methods=["GET"])
def get_most_accurate(owner):
    # query the accuracy index and scan index by accuracy  
    response = table.query(
        IndexName="models_accuracy",
        Select="ALL_PROJECTED_ATTRIBUTES",
        ScanIndexForward=False,
        KeyConditionExpression=Key('owner').eq(owner),
    )
    latest = response["Items"][0]
    if latest:
        return json.dumps(latest)


if __name__ == '__main__':
    with app.app_context():
        dynamo.create_all()

    app.run(debug=True, host='0.0.0.0', port=8000)
