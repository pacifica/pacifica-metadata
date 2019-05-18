# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Endpoints for querying for status of data
- Endpoints for querying for reporting of data

## [0.10.1] - 2019-05-18
### Added
- Metadata model
  - Dublin Core additions
  - Files grouped by transactions
  - Instruments, Analytical Tools, Projects and Users
  - Arbitrary Relationships between above objects
  - Arbitrary Key Value Pairs for Files and Transactions
- Extended REST API for introspection of objects
- Endpoints for Uploading Metadata
- Notifications for changes in the system
  - Object update/create/delete
  - Ingest event
  - DOI related events
- Metadata Model Upgrade Process
- ReadtheDocs supported Sphinx docs
- REST API for sending and recieving data
  - PUT - Create an Object
  - POST - Update an Object
  - GET - Get an Object
  - DELETE - Delete an Object

### Changed
