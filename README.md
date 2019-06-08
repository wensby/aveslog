# birding
Tiny birding web application for learning purposes

## Local development testing
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
