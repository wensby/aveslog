#!/bin/bash

cd web-service
npx babel src/birding/static/script/src --out-dir src/birding/static/script --presets react-app/prod
