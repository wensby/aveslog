#!/bin/bash

# Parse Options

POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -f|--force-recreate)
      FORCE_RECREATE="$1"
      shift # past argument
      ;;
    *)
      POSITIONAL+=("$1")
      shift # past argument
      ;;
  esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

RUNNING=$(docker-compose -f docker-compose.test.yml ps -q test-web-service)
if [ -z "$RUNNING" ] || [ -n "$FORCE_RECREATE" ]; then
  echo "Recreating test containers"
  docker-compose -f docker-compose.test.yml down
  # Destroy test database, forcing creation of new one
  rm -rf volumes/test-database
  docker-compose -f docker-compose.test.yml up --build --detach
fi

docker exec -i -t test-web-service /run_tests.sh
