#!/bin/bash

python3.7 -m venv web-service/venv
source web-service/venv/bin/activate
pip install -q --upgrade pip
pip install -q -r web-service/requirements.txt
cd web-service/src/birding
python -m unittest discover -t ..
deactivate
