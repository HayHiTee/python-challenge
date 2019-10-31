# Coding Challenge App

A flask app for a coding challenge.

## Install:

You can use a virtual environment (conda, venv, etc):
```
conda env create -f environment.yml
source activate user-profiles
```

Or just pip install from the requirements file
``` 
pip install -r requirements.txt
```

## Running the code
set FLASK_APP = run.py
flask run

### Spin up the service

```
# start up local server
python -m run 
```

### Making Requests

```
curl -i "http://127.0.0.1:5000/users/{team/organization_name}"
```
### Test
```
python tests.py

OR

python -m unittest
```


## What'd I'd like to improve on...
    1.) Custom Errors Handling
    
    2.) Github and Bitbucket repo topics

