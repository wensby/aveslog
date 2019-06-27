# birding
Tiny birding web application for learning purposes

## Running the app locally
### Starting
The whole app can be run locally using the local-dev-docker.sh script. This
script can also be run with a specific service name as argument, to rebuild and
restart only the specified service.
### Mail
As to not send real emails when testing the application locally, the dispatched
emails are instead logged in the birding-web-service container through the flask
app logging utility. The fact that no MAIL\_SERVER environment variable is set
in the birding-web-service container triggers the MailDispatcherFactory to
create a MailDebugDispatcher instead of a real MailServiceDispatcher when
calling MailDispatcherFactory.create\_dispatcher().

## Running the tests

The tests are run inside docker containers to try to mimic the production
environment as much as possible. The script test.sh is the key to testing the
application, and to make running the tests often fast and easy, the test
containers are spun up the first time the script is run. Afterwards, running
the test script will just simply execute all the tests in the already running
containers, which is fast. Updating the code to test won't require restarting
the containers since, unlike the production containers, the application code
is accessed through volumes, instead of copied into the containters.

If you wish to force a recreation of the test-containers, you can just use the
-f --force-recreate flag to the test script.

You can run the tests with coverage, which will, upon completion, copy over the
html report from the container to the current worker directory and open it up.
