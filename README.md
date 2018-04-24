# intercom

## Development

To set up the project run:

```
$ make setup
```

To run the test suite run:

```
$ make test
```

## Release

* Bump version in google_analytics_client/__init__.py
* Add changes to CHANGELOG.rst
* Open PR with title "Release <version>"
* Ensure test's pass.
* Build + push dist to gemfury:

```
python setup.py sdist
curl -F package=@<file> https://i86zpxHycM-ihTvTHHb9@push.fury.io/trackmaven/
```

* Merge PR to master.
* Added release to GitHub https://github.com/TrackMaven/intercom/releases with changelog notes.
