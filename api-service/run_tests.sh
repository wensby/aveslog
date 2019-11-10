#!/bin/sh

while ! nc -z test-database-service 5432; do sleep 1; done

if [ -n "$1" ]; then
  rm .coverage
  rm -rf htmlcov
  coverage run --source birding -m unittest discover -s birding
  coverage html
else
  python -m unittest discover -s birding
fi
