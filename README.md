# Identity Service

FX Labs has many different systems generating currency trades.
So that our clients can easily look up individual trades, we
want to assign each trade its unique 7-character alphanumeric
human-readable ID.

Example: B762F00

An API will use this package to create new unique IDs on demand.

## Setup

You will need a Python environment with the package requirements
installed.

To set this up using `virtualenv`, run:

```
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

You can run the tests with:

```
$ python -m pytest
```

This is a FastAPI app. You can run it with:

```
$ fastapi dev app/main.py
```
