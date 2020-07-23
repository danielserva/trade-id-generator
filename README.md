================
Identity Service
================

FX Labs has many different systems generating currency trades.
So that our clients can look up individual trades easily, we
want to assign each trade its own unique 7 character alphanumeric
human readable ID.

Example: B762F00


This package will be used by an API to create new IDs on demand.


Setup
=====

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

Task
====

This repo contains tests for code to generate the IDs. You will need to
complete the code in `identity/generation.py`

The tests in `python-test` will run uniqueness and simple format checks.

After you have made these tests pass, please commit your changes
to the `python-test` branch.

There are further branches with more tests. Merge one branch at
a time into `python-test`, and commit your changes to `python-test`.

The branches are:

`origin/python-bulk-generation` - adds tests for a bulk generation function
to generate many IDs at once, and improves the uniqueness and formatting
tests.

`origin/python-concurrency` - tests that the code can handle many concurrent
requests in a multithreaded environment.

`origin/python-persistence-and-fault-tolerance` - tests that the code can
recover from crashes and restarts without duplicating IDs.

`origin/python-performance` - tests the code performance.

Your aim is to come up with the best solution you can within 3 hours.

Once you have finished, please create a git bundle to send back to
us with this command:

```
$ git bundle create repo.bundle --all
```

Good luck!
