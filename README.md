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

This repo contains tests for the ID generation code, the task is
to make these tests pass.

The tests in `master` will run uniqueness and simple format checks.

After you have made these tests pass, please commit your changes
to the `master` branch.

There are further branches with more tests. Merge one branch at
a time into `master`, then make the tests from that branch pass,
and commit your changes to `master`.

The branches are:

`origin/bulk-generation` - adds tests for a bulk generation function
to generate many IDs at once, and improves the uniqueness and formatting
tests.

`origin/concurrency` - tests that the code can handle many concurrent
requests.

`origin/persistence-and-fault-tolerance` - tests that the code can
recover from crashes and restarts without duplicating IDs.

Your aim is to make as many of the tests pass as possible within 3 hours.

Once you have finished, please create a git bundle to send back to
us with this command:

```
$ git bundle create repo.bundle --all
```

Good luck!
