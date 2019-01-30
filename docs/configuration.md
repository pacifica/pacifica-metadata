# Configuration

The Pacifica Core services require two configuration files. The REST
API utilizes [CherryPy](https://github.com/cherrypy) and review of
their
[configuration documentation](http://docs.cherrypy.org/en/latest/config.html)
is recommended. The service configuration file is a INI formatted
file containing configuration for database connections.

## CherryPy Configuration File

An example of Metadata server CherryPy configuration:

```ini
[global]
log.screen: True
log.access_file: 'access.log'
log.error_file: 'error.log'
server.socket_host: '0.0.0.0'
server.socket_port: 8121

[/]
request.dispatch: cherrypy.dispatch.MethodDispatcher()
tools.response_headers.on: True
tools.response_headers.headers: [('Content-Type', 'application/json')]
```

## Service Configuration File

The service configuration is an INI file and an example is as follows:

```ini
[database]
; This section contains database connection configuration

; peewee_url is defined as the URL PeeWee can consume.
; http://docs.peewee-orm.com/en/latest/peewee/database.html#connecting-using-a-database-url
peewee_url = postgresql://pacifica:metadata@localhost:5432/pacifica_metadata

; connect_attempts are the number of times the service will attempt to
; connect to the database if unavailable.
connect_attempts = 10

; connect_wait are the number of seconds the service will wait between
; connection attempts until a successful connection to the database.
connect_wait = 20

; enable debug logging of database queries
debug_logging = False

[notifications]
; This section describes where the notifications server is.

; Disable eventing for the metadata service.
disabled = False

; URL to the recieve endpoint on the notifications server.
url = http://127.0.0.1:8070/receive

[elasticsearch]
; This section describes configuration to contact elasticsearch

; URL to the elasticsearch server
url = http://127.0.0.1:9200
```

## Starting the Service

Starting the Metadata service can be done by two methods. However,
understanding the requirements and how they apply to REST services
is important to address as well. Using the
internal CherryPy server to start the service is recommended for
Windows platforms. For Linux/Mac platforms it is recommended to
deploy the service with
[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).

### Deployment Considerations

The Metadata service is the authoritative metadata store for all data
in Pacifica. This means any queries needed by any other Pacifica
services goes through a REST endpoint on this service. As different
services require performance characteristics of each endpoint it is
important to have a deployment mechanism that behaves consistently.

The CherryPy service works well enough for many of the queries.
However, for performance and scalability using uWSGI is preferred.
Also putting system memory consumption limits on the service is
also recommended. As you get more data in the system some queries
will grow to consume memory beyond a single system.

As data volume in Pacifica and load on queries increase the Metadata
service works better running in uWSGI. The chance increases of a
query consuming all the system memory on the server. As CherryPy is
a threaded application Linux will kill the process to free up memory.
This results in the service going down entirely and not servicing
requests. uWSGI takes care of this by utilizing a forking model for
handling requests. Using uWSGI, a child process is killed and a 500
is returned to the client. uWSGI continues handling requests, cleans
up the dead child and spawns new ones.

### CherryPy Server

To make running the Metadata service using the CherryPy's builtin
server easier we have a command line entry point.

```
$ pacifica-metadata --help
usage: pacifica-metadata [-h] [--cpconfig CPCONFIG] [-c CONFIG] [-p PORT]
                         [-a ADDRESS]

Run the metadata server.

optional arguments:
  -h, --help            show this help message and exit
  --cpconfig CPCONFIG   cherrypy config file
  -c CONFIG, --config CONFIG
                        database config file
  -p PORT, --port PORT  port to listen on
  -a ADDRESS, --address ADDRESS
                        address to listen on
$ pacifica-metadata-cmd dbsync
$ pacifica-metadata
[09/Jan/2019:09:17:26] ENGINE Listening for SIGTERM.
[09/Jan/2019:09:17:26] ENGINE Bus STARTING
[09/Jan/2019:09:17:26] ENGINE Set handler for console events.
[09/Jan/2019:09:17:26] ENGINE Started monitor thread 'Autoreloader'.
[09/Jan/2019:09:17:26] ENGINE Serving on http://0.0.0.0:8121
[09/Jan/2019:09:17:26] ENGINE Bus STARTED
```

### uWSGI Server

To make running the UniqueID service using uWSGI easier we have a
module to be included as part of the uWSGI configuration. uWSGI is
very configurable and can use this module many different ways. Please
consult the
[uWSGI Configuration](https://uwsgi-docs.readthedocs.io/en/latest/Configuration.html)
documentation for more complicated deployments.

```
$ pip install uwsgi
$ uwsgi --http-socket :8121 --master --module pacifica.metadata.wsgi
```
