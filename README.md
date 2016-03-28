# Pacifica Metadata Services
[![Build Status](https://travis-ci.org/EMSL-MSC/pacifica-metadata.svg?branch=master)](https://travis-ci.org/EMSL-MSC/pacifica-metadata)

This is the pacifica metadata API.

This service provides metadata for all objects and relationships
between the objects that the other components want to share between
themselves.

## The API

There are many different types of objects that all get queried and
created the same way. We will only show the user object interface
here but there are more covered in the [metadata model]
(METADATA_MODEL.md) docs.

### Create an Object

To create an object issue an HTTP PUT request.

```
{
  "person_id": 127,
  "first_name": "John",
  "last_name": "Doe",
  "network_id": "guest"
}
```

Then put the file.
```
curl -X PUT -T foo.json http://localhost:8080/users
```
