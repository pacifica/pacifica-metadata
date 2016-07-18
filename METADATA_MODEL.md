# The Pacifica Metadata Model

This covers all the objects and their relationships to other
objects in the model.

## All The Objects

### Journals
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
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
| institution_name | TEXT |  |
| is_foreign | INTEGER |  |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Proposals
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| abstract | TEXT |  |
| accepted_date | TIMESTAMP |  |
| actual_end_date | TIMESTAMP |  |
| actual_start_date | TIMESTAMP |  |
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
| display_name | VARCHAR |  |
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
| user | INTEGER | Users.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Keywords
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| citation | INTEGER | Citations.id |
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
| hours_estimated | INTEGER |  |
| instrument | INTEGER | Instruments.id |
| proposal | INTEGER | Proposals.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### ProposalParticipant
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| member | INTEGER | Users.id |
| proposal | INTEGER | Proposals.id |
| proposal_author_sw | VARCHAR |  |
| proposal_co_author_sw | VARCHAR |  |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### CitationProposal
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| citation | INTEGER | Citations.id |
| proposal | INTEGER | Proposals.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Transactions
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| instrument | INTEGER | Instruments.id |
| proposal | INTEGER | Proposals.id |
| submitter | INTEGER | Users.id |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Files
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
| ctime | TIMESTAMP |  |
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
| key | VARCHAR |  |
| created | TIMESTAMP |  |
| deleted | TIMESTAMP |  |
| updated | TIMESTAMP |  |

### Values
| Column | Type | Reference |
| --- | --- | --- |
| id | SERIAL |  |
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


## Note
This document is generated by the ```gen-md-model-md.py``` script and needs to
be regenerated whenever changes are made to the model.

