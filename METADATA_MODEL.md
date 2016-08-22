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
| journal_name | VARCHAR |  |
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
| institution_name | TEXT |  |
| is_foreign | BOOLEAN |  |
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
| instrument_name | VARCHAR |  |
| name_short | VARCHAR |  |
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
| journal_id | INTEGER | Journals.id |
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
| institution_id | INTEGER | Institutions.id |
| last_name | VARCHAR |  |
| middle_initial | VARCHAR |  |
| person | INTEGER | Users.id |
| person_id | INTEGER | Users.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### InstitutionPerson
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| institution | INTEGER | Institutions.id |
| institution_id | INTEGER | Institutions.id |
| person | INTEGER | Users.id |
| person_id | INTEGER | Users.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Keywords
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| citation | INTEGER | Citations.id |
| citation_id | INTEGER | Citations.id |
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
| author_id | INTEGER | Contributors.id |
| author_precedence | INTEGER |  |
| citation | INTEGER | Citations.id |
| citation_id | INTEGER | Citations.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### ProposalInstrument
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| instrument | INTEGER | Instruments.id |
| instrument_id | INTEGER | Instruments.id |
| proposal | VARCHAR | Proposals.id |
| proposal_id | VARCHAR | Proposals.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### ProposalParticipant
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| person | INTEGER | Users.id |
| person_id | INTEGER | Users.id |
| proposal | VARCHAR | Proposals.id |
| proposal_author_sw | VARCHAR |  |
| proposal_co_author_sw | VARCHAR |  |
| proposal_id | VARCHAR | Proposals.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### CitationProposal
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| citation | INTEGER | Citations.id |
| citation_id | INTEGER | Citations.id |
| proposal | VARCHAR | Proposals.id |
| proposal_id | VARCHAR | Proposals.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Transactions
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| instrument | INTEGER | Instruments.id |
| instrument_id | INTEGER | Instruments.id |
| proposal | VARCHAR | Proposals.id |
| proposal_id | VARCHAR | Proposals.id |
| submitter | INTEGER | Users.id |
| submitter_id | INTEGER | Users.id |
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
| transaction_id | INTEGER | Transactions.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Keys
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
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
| file_id | INTEGER | Files.id |
| key | INTEGER | Keys.id |
| key_id | INTEGER | Keys.id |
| value | INTEGER | Values.id |
| value_id | INTEGER | Values.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### TransactionKeyValue
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| key | INTEGER | Keys.id |
| key_id | INTEGER | Keys.id |
| transaction | INTEGER | Transactions.id |
| transaction_id | INTEGER | Transactions.id |
| value | INTEGER | Values.id |
| value_id | INTEGER | Values.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Groups
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| encoding | VARCHAR |  |
| group_name | VARCHAR |  |
| is_admin | BOOLEAN |  |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### UserGroup
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| group | INTEGER | Groups.id |
| group_id | INTEGER | Groups.id |
| person | INTEGER | Users.id |
| person_id | INTEGER | Users.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### InstrumentGroup
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| group | INTEGER | Groups.id |
| group_id | INTEGER | Groups.id |
| instrument | INTEGER | Instruments.id |
| instrument_id | INTEGER | Instruments.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |


## Note
This document is generated by the ```gen-md-model-md.py``` script and needs to
be regenerated whenever changes are made to the model.

