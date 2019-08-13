# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Endpoints for querying for status of data
- Endpoints for querying for reporting of data

## [0.12.0] - 2019-08-12
### Changed
- Fix #247 and #246 spelling error and email lowercase [@dmlb2000](https://github.com/dmlb2000)
- Unlock psycopg2 dependency [@dmlb2000](https://github.com/dmlb2000)

## [0.11.1] - 2019-07-10
### Changed
- QuickFix #244 Missed column renames by [@dmlb2000](https://github.com/dmlb2000)

## [0.11.0] - 2019-07-10
### Changed
- Fix #240 Add Dataset model and relationships by [@dmlb2000](https://github.com/dmlb2000)
- Fix #238 Rename UserGroup column by [@dmlb2000](https://github.com/dmlb2000)
- Fix #236 Add Hashlist column operations by [@dmlb2000](https://github.com/dmlb2000)

## [0.10.3] - 2019-06-05
### Changed
- Fix #233 Loosen where clause for users by [@kauberry](https://github.com/kauberry)
- Fix #231 Update Docs by [@dmlb2000](https://github.com/dmlb2000)

## [0.10.2] - 2019-05-30
### Changed
- Fix #223 Add Nice Status Url by [@dmlb2000](https://github.com/dmlb2000)
- Fix #225 Add UUID check for JSON serialization [@dmlb2000](https://github.com/dmlb2000)
- Fix user lookup clause in user queries endpoint [@kauberry](https://github.com/kauberry)

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
