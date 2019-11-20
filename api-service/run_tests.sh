#!/bin/sh

while ! nc -z test-database-service 5432; do sleep 1; done

if [ -n "$1" ]; then
  rm .coverage
  rm -rf htmlcov
  coverage run --omit=*/test_*.py -m unittest discover -f
  coverage html
else
  python -m unittest discover -f -s aveslog
fi
