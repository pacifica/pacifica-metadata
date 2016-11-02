# The Pacifica Metadata Model

This covers all the objects and their relationships to other
objects in the model.

## All The Objects

### Journals
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| encoding | VARCHAR |  |
| impact_factor | REAL |  |
| name | VARCHAR |  |
| website_url | VARCHAR |  |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Users
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| email_address | VARCHAR |  |
| encoding | VARCHAR |  |
| first_name | VARCHAR |  |
| last_name | VARCHAR |  |
| middle_initial | VARCHAR |  |
| network_id | VARCHAR |  |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Institutions
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| association_cd | VARCHAR |  |
| encoding | VARCHAR |  |
| is_foreign | BOOLEAN |  |
| name | TEXT |  |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Proposals
| Column | Type | Reference |
| --- | --- | --- |
| id | VARCHAR |  |
| abstract | TEXT |  |
| accepted_date | DATE |  |
| actual_end_date | DATE |  |
| actual_start_date | DATE |  |
| closed_date | DATE |  |
| encoding | VARCHAR |  |
| proposal_type | VARCHAR |  |
| science_theme | VARCHAR |  |
| submitted_date | TIMESTAMP |  |
| title | TEXT |  |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Instruments
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| active | BOOLEAN |  |
| display_name | VARCHAR |  |
| encoding | VARCHAR |  |
| name | VARCHAR |  |
| name_short | VARCHAR |  |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### InstrumentCustodian
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| custodian | INTEGER | Users.id |
| instrument | INTEGER | Instruments.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Citations
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| abstract_text | TEXT |  |
| article_title | TEXT |  |
| doi_reference | VARCHAR |  |
| encoding | VARCHAR |  |
| journal | INTEGER | Journals.id |
| journal_issue | INTEGER |  |
| journal_volume | INTEGER |  |
| page_range | VARCHAR |  |
| release_authorization_id | VARCHAR |  |
| xml_text | TEXT |  |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Contributors
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| dept_code | VARCHAR |  |
| encoding | VARCHAR |  |
| first_name | VARCHAR |  |
| institution | INTEGER | Institutions.id |
| last_name | VARCHAR |  |
| middle_initial | VARCHAR |  |
| person | INTEGER | Users.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### InstitutionPerson
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| institution | INTEGER | Institutions.id |
| person | INTEGER | Users.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Keywords
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| citation | INTEGER | Citations.id |
| encoding | VARCHAR |  |
| keyword | VARCHAR |  |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### CitationContributor
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| author | INTEGER | Contributors.id |
| author_precedence | INTEGER |  |
| citation | INTEGER | Citations.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### ProposalInstrument
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| instrument | INTEGER | Instruments.id |
| proposal | VARCHAR | Proposals.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### ProposalParticipant
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| person | INTEGER | Users.id |
| proposal | VARCHAR | Proposals.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### CitationProposal
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| citation | INTEGER | Citations.id |
| proposal | VARCHAR | Proposals.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Transactions
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| instrument | INTEGER | Instruments.id |
| proposal | VARCHAR | Proposals.id |
| submitter | INTEGER | Users.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Files
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| ctime | TIMESTAMP |  |
| encoding | VARCHAR |  |
| mimetype | VARCHAR |  |
| mtime | TIMESTAMP |  |
| name | VARCHAR |  |
| size | BIGINT |  |
| subdir | VARCHAR |  |
| transaction | INTEGER | Transactions.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Keys
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| encoding | VARCHAR |  |
| key | VARCHAR |  |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Values
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| encoding | VARCHAR |  |
| value | VARCHAR |  |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### FileKeyValue
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| file | INTEGER | Files.id |
| key | INTEGER | Keys.id |
| value | INTEGER | Values.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### TransactionKeyValue
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| key | INTEGER | Keys.id |
| transaction | INTEGER | Transactions.id |
| value | INTEGER | Values.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Groups
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| encoding | VARCHAR |  |
| is_admin | BOOLEAN |  |
| name | VARCHAR |  |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### UserGroup
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| group | INTEGER | Groups.id |
| person | INTEGER | Users.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### InstrumentGroup
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| group | INTEGER | Groups.id |
| instrument | INTEGER | Instruments.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### AnalyticalTools
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| encoding | VARCHAR |  |
| name | VARCHAR |  |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### AToolProposal
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| analytical_tool | INTEGER | AnalyticalTools.id |
| proposal | VARCHAR | Proposals.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### AToolTransaction
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| analytical_tool | INTEGER | AnalyticalTools.id |
| transaction | INTEGER | Transactions.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |


## Note
This document is generated by the ```GenMetadataModelMD.py``` script and needs to
be regenerated whenever changes are made to the model.
