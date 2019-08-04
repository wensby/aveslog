#!/bin/sh

# Recreate config file
rm -rf ./env-config.js
touch ./env-config.js

echo "window._env_ = {" >> ./env-config.js
echo "  API_URL: \"$API_URL\"," >> ./env-config.js
echo "}" >> ./env-config.js

mv ./env-config.js ./public/env-config.js
