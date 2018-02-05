# The Pacifica Metadata Model

This covers all the objects and their relationships to other
objects in the model.

## All The Objects

### Journals
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| encoding | VARCHAR |  | NOT NULL |
| impact_factor | REAL |  | NOT NULL |
| name | VARCHAR |  | NOT NULL |
| website_url | VARCHAR |  | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### Users
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| email_address | VARCHAR |  | NOT NULL |
| encoding | VARCHAR |  | NOT NULL |
| first_name | VARCHAR |  | NOT NULL |
| last_name | VARCHAR |  | NOT NULL |
| middle_initial | VARCHAR |  | NOT NULL |
| network_id | VARCHAR |  | NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### Institutions
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| association_cd | VARCHAR |  | NOT NULL |
| encoding | VARCHAR |  | NOT NULL |
| is_foreign | BOOLEAN |  | NOT NULL |
| name | TEXT |  | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### Proposals
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | VARCHAR |  | NOT NULL, PRIMARY KEY |
| abstract | TEXT |  | NOT NULL |
| accepted_date | DATE |  | NULL |
| actual_end_date | DATE |  | NULL |
| actual_start_date | DATE |  | NULL |
| closed_date | DATE |  | NULL |
| encoding | VARCHAR |  | NOT NULL |
| proposal_type | VARCHAR |  | NOT NULL |
| science_theme | VARCHAR |  | NULL |
| short_name | VARCHAR |  | NOT NULL |
| submitted_date | TIMESTAMP |  | NOT NULL |
| suspense_date | DATE |  | NULL |
| title | TEXT |  | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### Instruments
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| active | BOOLEAN |  | NOT NULL |
| display_name | VARCHAR |  | NOT NULL |
| encoding | VARCHAR |  | NOT NULL |
| name | VARCHAR |  | NOT NULL |
| name_short | VARCHAR |  | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### InstrumentCustodian
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| custodian | INTEGER | Users.id | NOT NULL |
| instrument | INTEGER | Instruments.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### Citations
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| abstract_text | TEXT |  | NOT NULL |
| article_title | TEXT |  | NOT NULL |
| doi_reference | VARCHAR |  | NOT NULL |
| encoding | VARCHAR |  | NOT NULL |
| journal | INTEGER | Journals.id | NOT NULL |
| journal_issue | INTEGER |  | NOT NULL |
| journal_volume | INTEGER |  | NOT NULL |
| page_range | VARCHAR |  | NOT NULL |
| release_authorization_id | VARCHAR |  | NOT NULL |
| xml_text | TEXT |  | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### Contributors
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| dept_code | VARCHAR |  | NOT NULL |
| encoding | VARCHAR |  | NOT NULL |
| first_name | VARCHAR |  | NOT NULL |
| institution | INTEGER | Institutions.id | NOT NULL |
| last_name | VARCHAR |  | NOT NULL |
| middle_initial | VARCHAR |  | NOT NULL |
| person | INTEGER | Users.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### InstitutionPerson
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| institution | INTEGER | Institutions.id | NOT NULL |
| person | INTEGER | Users.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### Keywords
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| encoding | VARCHAR |  | NOT NULL |
| keyword | VARCHAR |  | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### CitationContributor
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| author | INTEGER | Contributors.id | NOT NULL |
| author_precedence | INTEGER |  | NOT NULL |
| citation | INTEGER | Citations.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### CitationKeyword
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| citation | INTEGER | Citations.id | NOT NULL |
| keyword | INTEGER | Keywords.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### ProposalInstrument
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| instrument | INTEGER | Instruments.id | NOT NULL |
| proposal | VARCHAR | Proposals.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### ProposalParticipant
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| person | INTEGER | Users.id | NOT NULL |
| proposal | VARCHAR | Proposals.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### CitationProposal
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| citation | INTEGER | Citations.id | NOT NULL |
| proposal | VARCHAR | Proposals.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### Transactions
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| instrument | INTEGER | Instruments.id | NOT NULL |
| proposal | VARCHAR | Proposals.id | NOT NULL |
| submitter | INTEGER | Users.id | NOT NULL |
| suspense_date | DATE |  | NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### Files
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| ctime | TIMESTAMP |  | NOT NULL |
| encoding | VARCHAR |  | NOT NULL |
| hashsum | VARCHAR |  | NOT NULL |
| hashtype | VARCHAR |  | NOT NULL |
| mimetype | VARCHAR |  | NOT NULL |
| mtime | TIMESTAMP |  | NOT NULL |
| name | VARCHAR |  | NOT NULL |
| size | BIGINT |  | NOT NULL |
| subdir | VARCHAR |  | NOT NULL |
| suspense_date | DATE |  | NULL |
| transaction | INTEGER | Transactions.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### Keys
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| encoding | VARCHAR |  | NOT NULL |
| key | VARCHAR |  | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### Values
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| encoding | VARCHAR |  | NOT NULL |
| value | VARCHAR |  | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### FileKeyValue
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| file | INTEGER | Files.id | NOT NULL |
| key | INTEGER | Keys.id | NOT NULL |
| value | INTEGER | Values.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### TransactionKeyValue
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| key | INTEGER | Keys.id | NOT NULL |
| transaction | INTEGER | Transactions.id | NOT NULL |
| value | INTEGER | Values.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### Groups
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| encoding | VARCHAR |  | NOT NULL |
| is_admin | BOOLEAN |  | NOT NULL |
| name | VARCHAR |  | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### UserGroup
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| group | INTEGER | Groups.id | NOT NULL |
| person | INTEGER | Users.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### InstrumentGroup
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| group | INTEGER | Groups.id | NOT NULL |
| instrument | INTEGER | Instruments.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### AnalyticalTools
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| encoding | VARCHAR |  | NOT NULL |
| name | VARCHAR |  | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### AToolProposal
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| analytical_tool | INTEGER | AnalyticalTools.id | NOT NULL |
| proposal | VARCHAR | Proposals.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### AToolTransaction
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| analytical_tool | INTEGER | AnalyticalTools.id | NOT NULL |
| transaction | INTEGER | Transactions.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### DOIDataSets
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| doi | VARCHAR |  | NOT NULL |
| encoding | VARCHAR |  | NOT NULL |
| name | VARCHAR |  | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |

### DOIResource
| Column | Type | Reference | Attributes |
| --- | --- | --- | --- |
| id | SERIAL |  | NOT NULL, PRIMARY KEY |
| doi | VARCHAR | DOIDataSets.doi | NOT NULL |
| transaction | INTEGER | Transactions.id | NOT NULL |
| created | TIMESTAMP |  | NOT NULL |
| deleted | TIMESTAMP |  | NULL |
| updated | TIMESTAMP |  | NOT NULL |


## Note
This document is generated by the ```GenMetadataModelMD.py``` script and needs to
be regenerated whenever changes are made to the model.
