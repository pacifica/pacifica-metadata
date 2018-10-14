# The Pacifica Metadata Model

This covers all the objects and their relationships to other
objects in the model.

## All The Objects

### Journals
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | PrimaryKeyField |  | NOT NULL, PRIMARY KEY |
| name | CharField |  | NOT NULL |
| impact_factor | FloatField |  | NOT NULL |
| website_url | CharField |  | NOT NULL |
| encoding | CharField |  | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### Users
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | PrimaryKeyField |  | NOT NULL, PRIMARY KEY |
| first_name | CharField |  | NOT NULL |
| middle_initial | CharField |  | NOT NULL |
| last_name | CharField |  | NOT NULL |
| network_id | CharField |  | NULL |
| email_address | CharField |  | NOT NULL |
| encoding | CharField |  | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### Institutions
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | PrimaryKeyField |  | NOT NULL, PRIMARY KEY |
| name | TextField |  | NOT NULL |
| association_cd | CharField |  | NOT NULL |
| is_foreign | BooleanField |  | NOT NULL |
| encoding | CharField |  | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### Proposals
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | CharField |  | NOT NULL, PRIMARY KEY |
| title | TextField |  | NOT NULL |
| short_name | CharField |  | NULL |
| abstract | TextField |  | NULL |
| science_theme | CharField |  | NULL |
| proposal_type | CharField |  | NULL |
| submitted_date | ExtendDateTimeField |  | NOT NULL |
| accepted_date | ExtendDateField |  | NULL |
| actual_start_date | ExtendDateField |  | NULL |
| actual_end_date | ExtendDateField |  | NULL |
| closed_date | ExtendDateField |  | NULL |
| suspense_date | ExtendDateField |  | NULL |
| encoding | CharField |  | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### Instruments
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | PrimaryKeyField |  | NOT NULL, PRIMARY KEY |
| display_name | CharField |  | NOT NULL |
| name | CharField |  | NOT NULL |
| name_short | CharField |  | NOT NULL |
| active | BooleanField |  | NOT NULL |
| encoding | CharField |  | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### InstrumentCustodian
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| instrument | ForeignKeyField | Instruments.id | NOT NULL |
| custodian | ForeignKeyField | Users.id | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### Citations
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | PrimaryKeyField |  | NOT NULL, PRIMARY KEY |
| article_title | TextField |  | NOT NULL |
| journal | ForeignKeyField | Journals.id | NOT NULL |
| journal_volume | IntegerField |  | NOT NULL |
| journal_issue | IntegerField |  | NOT NULL |
| page_range | CharField |  | NOT NULL |
| abstract_text | TextField |  | NOT NULL |
| xml_text | TextField |  | NOT NULL |
| release_authorization_id | CharField |  | NOT NULL |
| doi_reference | CharField |  | NOT NULL |
| encoding | CharField |  | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### Contributors
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | PrimaryKeyField |  | NOT NULL, PRIMARY KEY |
| person | ForeignKeyField | Users.id | NOT NULL |
| first_name | CharField |  | NOT NULL |
| middle_initial | CharField |  | NOT NULL |
| last_name | CharField |  | NOT NULL |
| dept_code | CharField |  | NOT NULL |
| institution | ForeignKeyField | Institutions.id | NOT NULL |
| encoding | CharField |  | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### InstitutionPerson
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| person | ForeignKeyField | Users.id | NOT NULL |
| institution | ForeignKeyField | Institutions.id | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### Keywords
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | PrimaryKeyField |  | NOT NULL, PRIMARY KEY |
| keyword | CharField |  | NOT NULL |
| encoding | CharField |  | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### CitationContributor
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| citation | ForeignKeyField | Citations.id | NOT NULL |
| author | ForeignKeyField | Contributors.id | NOT NULL |
| author_precedence | IntegerField |  | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### CitationKeyword
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| citation | ForeignKeyField | Citations.id | NOT NULL |
| keyword | ForeignKeyField | Keywords.id | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### ProposalInstrument
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| instrument | ForeignKeyField | Instruments.id | NOT NULL |
| proposal | ForeignKeyField | Proposals.id | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### ProposalParticipant
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| person | ForeignKeyField | Users.id | NOT NULL |
| proposal | ForeignKeyField | Proposals.id | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### CitationProposal
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| citation | ForeignKeyField | Citations.id | NOT NULL |
| proposal | ForeignKeyField | Proposals.id | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### Transactions
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | PrimaryKeyField |  | NOT NULL, PRIMARY KEY |
| submitter | ForeignKeyField | Users.id | NOT NULL |
| instrument | ForeignKeyField | Instruments.id | NOT NULL |
| proposal | ForeignKeyField | Proposals.id | NOT NULL |
| suspense_date | ExtendDateField |  | NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### Files
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | PrimaryKeyField |  | NOT NULL, PRIMARY KEY |
| name | CharField |  | NOT NULL |
| subdir | CharField |  | NOT NULL |
| ctime | ExtendDateTimeField |  | NOT NULL |
| mtime | ExtendDateTimeField |  | NOT NULL |
| hashsum | CharField |  | NOT NULL |
| hashtype | CharField |  | NOT NULL |
| size | BigIntegerField |  | NOT NULL |
| transaction | ForeignKeyField | Transactions.id | NOT NULL |
| mimetype | CharField |  | NOT NULL |
| encoding | CharField |  | NOT NULL |
| suspense_date | ExtendDateField |  | NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### Keys
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | PrimaryKeyField |  | NOT NULL, PRIMARY KEY |
| key | CharField |  | NOT NULL |
| encoding | CharField |  | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### Values
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | PrimaryKeyField |  | NOT NULL, PRIMARY KEY |
| value | CharField |  | NOT NULL |
| encoding | CharField |  | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### FileKeyValue
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| file | ForeignKeyField | Files.id | NOT NULL |
| key | ForeignKeyField | Keys.id | NOT NULL |
| value | ForeignKeyField | Values.id | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### TransactionKeyValue
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| transaction | ForeignKeyField | Transactions.id | NOT NULL |
| key | ForeignKeyField | Keys.id | NOT NULL |
| value | ForeignKeyField | Values.id | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### Groups
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | PrimaryKeyField |  | NOT NULL, PRIMARY KEY |
| name | CharField |  | NOT NULL |
| is_admin | BooleanField |  | NOT NULL |
| encoding | CharField |  | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### UserGroup
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| person | ForeignKeyField | Users.id | NOT NULL |
| group | ForeignKeyField | Groups.id | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### InstrumentGroup
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| instrument | ForeignKeyField | Instruments.id | NOT NULL |
| group | ForeignKeyField | Groups.id | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### AnalyticalTools
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | PrimaryKeyField |  | NOT NULL, PRIMARY KEY |
| name | CharField |  | NOT NULL |
| encoding | CharField |  | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### AToolProposal
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| proposal | ForeignKeyField | Proposals.id | NOT NULL |
| analytical_tool | ForeignKeyField | AnalyticalTools.id | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### AToolTransaction
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| transaction | ForeignKeyField | Transactions.id | NOT NULL |
| analytical_tool | ForeignKeyField | AnalyticalTools.id | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### TransactionRelease
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| transaction | ForeignKeyField | Transactions.id | NOT NULL, PRIMARY KEY |
| authorized_person | ForeignKeyField | Users.id | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### DOIEntries
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| doi | CharField |  | NOT NULL, PRIMARY KEY |
| status | CharField |  | NOT NULL |
| site_url | CharField |  | NOT NULL |
| encoding | CharField |  | NOT NULL |
| creator | ForeignKeyField | Users.id | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### DOIAuthors
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | PrimaryKeyField |  | NOT NULL, PRIMARY KEY |
| last_name | CharField |  | NOT NULL |
| first_name | CharField |  | NOT NULL |
| email | CharField |  | NULL |
| affiliation | CharField |  | NULL |
| orcid | CharField |  | NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### DOITransaction
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| doi | ForeignKeyField | DOIEntries.doi | NOT NULL, PRIMARY KEY |
| transaction | ForeignKeyField | TransactionRelease.transaction | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### CitationTransaction
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| citation | ForeignKeyField | Citations.id | NOT NULL |
| transaction | ForeignKeyField | TransactionRelease.transaction | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### CitationDOI
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| doi | ForeignKeyField | DOIEntries.doi | NOT NULL |
| citation | ForeignKeyField | Citations.id | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### DOIAuthorMapping
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| author | ForeignKeyField | DOIAuthors.id | NOT NULL |
| doi | ForeignKeyField | DOIEntries.doi | NOT NULL |
| author_order | IntegerField |  | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |

### DOIInfo
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| doi | ForeignKeyField | DOIEntries.doi | NOT NULL |
| key | CharField |  | NOT NULL |
| value | CharField |  | NOT NULL |
| version | CharField |  | NOT NULL |
| created | ExtendDateTimeField |  | NOT NULL |
| updated | ExtendDateTimeField |  | NOT NULL |
| deleted | ExtendDateTimeField |  | NULL |


## Note
This document is generated by the ```GenMetadataModelMD.py``` script and needs to
be regenerated whenever changes are made to the model.
