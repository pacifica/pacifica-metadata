# Pacifica Metadata Services
[![Build Status](https://travis-ci.org/pacifica/pacifica-metadata.svg?branch=master)](https://travis-ci.org/pacifica/pacifica-metadata)
[![Code Climate](https://codeclimate.com/github/pacifica/pacifica-metadata/badges/gpa.svg)](https://codeclimate.com/github/pacifica/pacifica-metadata)
[![Test Coverage](https://codeclimate.com/github/pacifica/pacifica-metadata/badges/coverage.svg)](https://codeclimate.com/github/pacifica/pacifica-metadata/coverage)
[![Issue Count](https://codeclimate.com/github/pacifica/pacifica-metadata/badges/issue_count.svg)](https://codeclimate.com/github/pacifica/pacifica-metadata)
[![Docker Stars](https://img.shields.io/docker/stars/pacifica/metadata.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/metadata/general)
[![Docker Pulls](https://img.shields.io/docker/pulls/pacifica/metadata.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/metadata/general)
[![Docker Automated build](https://img.shields.io/docker/automated/pacifica/metadata.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/metadata/builds)

This is the pacifica metadata API.

This service provides metadata for all objects and relationships
between the objects that the other components want to share between
themselves.

## Installing the Service

### Use the docker container

```
docker pull pacifica/metadata
```

### The Docker Compose Way

```
docker-compose up
```

### The Manual Way

Install the dependencies using pip (or some other similar python way).
```
pip install -r requirements.txt
```

Run the code.
```
python MetadataServer.py
```

## The API

There are many different types of objects that all get queried and
created the same way. We will only show the user object interface
here but there are more covered in the [metadata model]
(METADATA_MODEL.md) docs.

### Create an Object

To create an object issue an HTTP PUT request.

```
{
  "_id": 127,
  "first_name": "John",
  "last_name": "Doe",
  "network_id": "guest"
}
```

Then put the file.
```
curl -X PUT -T foo.json http://localhost:8121/users
```

### Get the Object

To get the object just created issue an HTTP GET request.

```
curl http://localhost:8121/users?_id=127
{
  "updated": 1459204793,
  "last_name": "Doe",
  "created": 1459204793,
  "deleted": 0,
  "first_name": "John",
  "network_id": "guest",
  "_id": 127
}
```

Optionally query on any other parts of the object.

```
curl http://localhost:8121/users?last_name=Doe&first_name=John
{
  "updated": 1459204793,
  "last_name": "Doe",
  "created": 1459204793,
  "deleted": 0,
  "first_name": "John",
  "network_id": "guest",
  "_id": 127
}
```

### Update the Object

To update the object with new data use the get args to identify the
object and post data to update the attributes of the object.

```
{
  "network_id": "jdoe"
}
```

Issue the POST
```
curl -X POST -T update.json 'http://localhost:8121/users?last_name=Doe&first_name=John'
```

Get the object to make sure it stuck.
```
{
  "updated": 1459205143,
  "last_name": "Doe",
  "created": 1459204793,
  "deleted": 0,
  "first_name": "John",
  "network_id": "jdoe",
  "_id": 127
}
```

*Notice* the updated field did change to the current time when the
POST happened.

### Delete the Object

To delete the object issue an HTTP DELETE request.
```
curl -X DELETE 'http://localhost:8121/users?_id=127'
```

*Notice* the deleted field is set on the object but the object isn't
really deleted.

```
curl http://localhost:8121/users?_id=127
{
  "updated": 1459205143,
  "last_name": "Doe",
  "created": 1459204793,
  "deleted": 1459205341,
  "first_name": "John",
  "network_id": "jdoe",
  "_id": 127
}
```

## Contributions

Contributions are accepted on github via the fork and pull request
workflow. Github has a good [help article]
(https://help.github.com/articles/using-pull-requests/) if you are
unfamiliar with this method of contributing.
