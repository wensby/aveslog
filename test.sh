#!/bin/bash

# Parse Options

POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -s|--setup) # Setup environment, used first time, or on changes
      SETUP="$1"
      shift # past argument
      ;;
    *)
      POSITIONAL+=("$1")
      shift # past argument
      ;;
  esac
done

if ! [ -z "$SETUP" ]; then
  python3.7 -m venv web-service/venv
fi

source web-service/venv/bin/activate

if ! [ -z "$SETUP" ]; then
  pip install -q --upgrade pip
  pip install -q -r web-service/requirements.txt
fi

cd web-service/src
python -m unittest discover -s tests
deactivate
