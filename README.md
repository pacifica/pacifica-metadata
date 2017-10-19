# Pacifica Metadata Services
[![Build Status](https://travis-ci.org/pacifica/pacifica-metadata.svg?branch=master)](https://travis-ci.org/pacifica/pacifica-metadata)
[![Code Climate](https://codeclimate.com/github/pacifica/pacifica-metadata/badges/gpa.svg)](https://codeclimate.com/github/pacifica/pacifica-metadata)
[![Test Coverage](https://codeclimate.com/github/pacifica/pacifica-metadata/badges/coverage.svg)](https://codeclimate.com/github/pacifica/pacifica-metadata/coverage)
[![Issue Count](https://codeclimate.com/github/pacifica/pacifica-metadata/badges/issue_count.svg)](https://codeclimate.com/github/pacifica/pacifica-metadata)
[![Docker Stars](https://img.shields.io/docker/stars/pacifica/metadata.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/metadata/general)
[![Docker Pulls](https://img.shields.io/docker/pulls/pacifica/metadata.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/metadata/general)
[![Docker Automated build](https://img.shields.io/docker/automated/pacifica/metadata.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/metadata/builds)

This is the Pacifica Metadata Services API.

This service provides metadata for objects and relationships between objects.
See the [metadata model](METADATA_MODEL.md) page for a complete listing of objects and relationships between objects.

## Installing the Service

### Use the Docker Container

```sh
docker pull pacifica/metadata
```

### The Docker Compose Way

```sh
docker-compose up
```

### The Manual Way

Install the dependencies using the `pip` command:

```sh
pip install -r requirements.txt
```

Then, run the code:

```sh
python MetadataServer.py
```

## The API

The Pacifica Metadata Services API covers the complete object life-cycle: create, read, update, and delete.

The examples in this section demonstrate the life-cycle of the `User` object using a Pacifica Metadata Services deployment at http://localhost:8121/ (see "Installing the Service" section).

### Creating an Object

To create a new `User` object, start by generating a new file `create.json` to store the JSON data:

```json
{
  "_id": 127,
  "email_address": "john@doe.com",
  "first_name": "John",
  "last_name": "Doe",
  "middle_initial": "",
  "network_id": "guest"
}
```

Then, provide the contents of the new file as the body for a HTTP PUT request using the `curl` command:

```sh
curl -X PUT -T create.json 'http://localhost:8121/users'
```

### Reading an Object

To retrieve the JSON data for the `User` object that was just created, send a HTTP GET request (with the `_id` attribute as a query parameter) using the `curl` command:

```sh
curl -X GET 'http://localhost:8121/users?_id=127'
```

The response body is a JSON array of JSON objects.
Because the query uses the `_id` attribute, a primary key, the JSON array contains either zero (no match) or one (match) JSON objects:

```json
[
  {
    "_id": 127,
    "email_address": "john@doe.com",
    "encoding": "UTF8",
    "first_name": "John",
    "last_name": "Doe",
    "middle_initial": "",
    "network_id": "guest",
    "created": 1459204793,
    "deleted": null,
    "updated": 1459204793
  }
]
```

Optionally, query on any other parts of an object by using its attributes as query parameters, e.g., to query on both the `first_name` and `last_name` attributes using the `curl` command:

```
curl -X GET 'http://localhost:8121/users?last_name=Doe&first_name=John'
```

Response bodies for queries on other parts may contain JSON data for more than one match:

```json
[
  {
    "_id": 127,
    "email_address": "john@doe.com",
    "encoding": "UTF8",
    "first_name": "John",
    "last_name": "Doe",
    "middle_initial": "",
    "network_id": "guest",
    "created": 1459204793,
    "deleted": null,
    "updated": 1459204793
  },
  ...
]
```

### Updating an Object

To modify a preexisting object, use the query parameters to identify the
object (or objects) and then send a HTTP POST request with the JSON data for the modified attributes as the request body, e.g., to modify the `network_id` attribute, start by generating a new file `update.json` to store the JSON data:

```json
{
  "network_id": "example"
}
```

Then, provide the contents of the new file as the body for a HTTP POST request using the `curl` command:

```sh
curl -X POST -T update.json 'http://localhost:8121/users?last_name=Doe&first_name=John'
```

Finally, verify the modifications by retrieving the most recent version of the object (see "Reading an Object" section), e.g., using the `curl` command:

```sh
curl -X GET 'http://localhost:8121/users?_id=127'
```

The `updated` attribute is automatically set to the current time when an object is modified:

```json
[
  {
    "_id": 127,
    "email_address": "john@doe.com",
    "encoding": "UTF8",
    "first_name": "John",
    "last_name": "Doe",
    "middle_initial": "",
    "network_id": "example",
    "created": 1459204793,
    "deleted": null,
    "updated": 1459205143
  }
]
```

### (Soft) Deleting an Object

To mark an object as `deleted`, i.e., to "soft delete" an object, send a HTTP DELETE request using the `curl` command:

```sh
curl -X DELETE 'http://localhost:8121/users?_id=127'
```

**NOTE** Don't worry! The object isn't really deleted.

Finally, verify the "soft delete" by retrieving the most recent version of the object (see "Reading an Object" section), e.g., using the `curl` command:

```sh
curl -X GET 'http://localhost:8121/users?_id=127'
```

The `deleted` attribute is automatically set to the current time when an object is "soft deleted":

```json
[
  {
    "_id": 127,
    "email_address": "john@doe.com",
    "encoding": "UTF8",
    "first_name": "John",
    "last_name": "Doe",
    "middle_initial": "",
    "network_id": "example",
    "created": 1459204793,
    "deleted": 1459205341,
    "updated": 1459205143
  }
]
```

## Contributions

Contributions are accepted on GitHub via the fork and pull request
workflow.
GitHub has a good [help article](https://help.github.com/articles/using-pull-requests/)
if you are unfamiliar with this method of contributing.
