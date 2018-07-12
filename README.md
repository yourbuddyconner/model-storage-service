# Model Storage Service

## Immediate Improvements That Could Be Made:
- Stricter validation at create endpoint.
- Caching to reduce DynamoDB queries. 
- Authentication at create endpoint. 
- Tests for all endpoints. 

## To Run: 
```
$ make up 
```


## CLI
```
$ python model_cli.py --help
Usage: model_cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create_model
  delete_model
  get_model
  most_accurate
  most_recent

```

## Endpoints: 

### Create Model
```
POST /models/
```

Parameters: 
- name: String
- owner: String
- accuracy: Float
- hyperparameters: Object
- feature_types: Array
- train_start: Integer
- train_stop: Integer

CuRL Command: 
```
curl --request POST \
  --url http://localhost:8000/models/ \
  --header 'content-type: application/json' \
  --data '{
	"name": "retention_model",
	"owner": "conner",
	"accuracy": 0.9999,
	"hyperparameters": { "hidden_layers": [4,2] },
	"feature_names": ["industry", "years_of_experience"],
	"train_start": 1531335810,
	"train_stop": 1631355810
}
'
```

CLI Command: 
```
python model_cli.py create_model --name=retention_model --accuracy=0.01 --owner=conner --feature_names="['industry', 'years_of_experience']" --hyperparameters="{ 'hidden_layers': [4,2] }" --train_start=1531335810 --train_stop=1531336810

```

Response: 
```
{
  "accuracy": 0.01,
  "feature_names": [
    "industry",
    "years_of_experience"
  ],
  "hyperparameters": {
    "hidden_layers": [
      4,
      2
    ]
  },
  "id": "ae75d908b5b73da62f0c93147e35a317",
  "name": "retention_model",
  "owner": "conner",
  "train_start": 1531335810,
  "train_stop": 1531336810
}
```

### Get Model 
```
GET /models/<id>
```

CuRL Command: 
```
curl --request GET \
  --url http://localhost:8000/models/7894066928b8e0ed7600c9fb14a3d2eb
```

CLI Command: 
```
python model_cli.py get_model --id=ae75d908b5b73da62f0c93147e35a317
```

Response: 
```
{
  "accuracy": 0.01,
  "feature_names": [
    "industry",
    "years_of_experience"
  ],
  "hyperparameters": {
    "hidden_layers": [
      4,
      2
    ]
  },
  "id": "ae75d908b5b73da62f0c93147e35a317",
  "name": "retention_model",
  "owner": "conner",
  "train_start": 1531335810,
  "train_stop": 1531336810
}
```

### Delete Model
```
DELETE /models/<id>
```

CuRL Command: 
```
curl --request DELETE \
  --url http://localhost:8000/models/7894066928b8e0ed7600c9fb14a3d2eb
```

CLI Command: 
```
python model_cli.py delete_model --id=ae75d908b5b73da62f0c93147e35a317
```

Response: 
```
{"deleted": true}
```

### Most Accurately Trained Model (By Owner)
```
GET /models/<owner>/most-accurate
```

CuRL Command: 
```
curl --request GET \
  --url http://localhost:8000/models/conner/most-accurate
```

CLI Command: 
```
python model_cli.py most_accurate --owner=conner
```

Response: 
```
{
  "accuracy": 4.09999,
  "feature_names": [
    "industry",
    "years_of_experience"
  ],
  "hyperparameters": {
    "hidden_layers": [
      4,
      2
    ]
  },
  "id": "7894066928b8e0ed7600c9fb14a3d2eb",
  "name": "retention_model",
  "owner": "conner",
  "train_start": 1531335810,
  "train_stop": 1641355810
}
```

### Most Recently Trained Model (By Owner)
```
GET /models/<owner>/most-recent
```

CuRL Command: 
```
curl --request GET \
  --url http://localhost:8000/models/conner/most-recent
```

CLI Command: 
```
python model_cli.py most_recent --owner=conner
```

Response: 
```
{
  "accuracy": 4.09999,
  "feature_names": [
    "industry",
    "years_of_experience"
  ],
  "hyperparameters": {
    "hidden_layers": [
      4,
      2
    ]
  },
  "id": "7894066928b8e0ed7600c9fb14a3d2eb",
  "name": "retention_model",
  "owner": "conner",
  "train_start": 1531335810,
  "train_stop": 1641355810
}
```
