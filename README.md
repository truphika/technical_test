# Network Coverage API

This is a simple API built using FastAPI for the Papernest Technical Test.

## Dependencies
### Required Dataset

This application requires a dataset to function, which is provided in the data folder. By default, the application uses this dataset. If you wish to use a different dataset, you can set the DATASET_PATH environment variable to point to your custom CSV file.

The dataset must follow the exact same structure as the default one. Any changes in the structure could lead to errors.
Installing Poetry

### Installing Poetry

Before installing dependencies, ensure Poetry is installed. You can install Poetry using pipx by running the following commands:

- Install pipx:
```
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

- Install Poetry:
```
pipx install poetry
```

Alternatively, you can follow the installation instructions from the official Poetry website: [Poetry Installation](https://python-poetry.org/docs/).

### Installing Python Dependencies
Once Poetry is installed, you can install the project's Python dependencies.
```
poetry install
```

## Start the Application

To run the application locally in development mode, use the following command:
```
poetry run fastapi dev src/api/main.py
```

Using a Custom Dataset

If you'd like to use a different dataset, set the DATASET_PATH environment variable like this:
```
DATASET_PATH=data/test.csv poetry run fastapi dev src/api/main.py
```

With the application running, you can access the Swagger UI documentation at:
http://127.0.0.1:8000/docs

## Testing the Endpoint

You can test the /network_coverage endpoint using Swagger UI or cURL. Here's an example of how to send a POST request with cURL:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/network_coverage' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": "157 boulevard Mac Donald 75019 Paris"
}'
```
## Run the Test Suite

To run the test suite, use the following command:
```
poetry run pytest
```
## Locate the Logs

The application logs to the console at a debug level by default.

Additionally, the application rotates log files and stores them in the logs folder.
### Changing the Log Level

If you wish to change the log level to something other than debug (e.g., info), you can set the LOG_LEVEL environment variable:
```
LOG_LEVEL=INFO poetry run fastapi dev src/api/main.py
```