#!/bin/sh

while ! nc -z test-database-service 5432; do sleep 1; done
python -m unittest discover -s tests
