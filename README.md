# Pacifica Metadata Services
[![Build Status](https://travis-ci.org/EMSL-MSC/pacifica-metadata.svg?branch=master)](https://travis-ci.org/EMSL-MSC/pacifica-metadata)

## Transfer Script ##
The **`EUSTransferSync`** script is written for the Python 2.7 runtime. This script looks in the **`SyncSettings(Dev/Prod).py`** file for its database connection string info and a list of tables to be mirrored over from EUS. Currently, two different files are present: **`SyncSettingsDev`** and **`SyncSettingsProd`**. These refer to the development settings and production settings to be used for the transfer script.

Look in **`EUSTransferSync.py`** around line 16 to switch from Dev to Prod settings (This needs to be a command line option eventually)

Change...

    from SyncSettingsDev import SOURCE_DATABASE_CREDS, DESTINATION_DATABASE_CREDS, TRANSFER_QUEUE_LIST
    
to

    from SyncSettingsProd import SOURCE_DATABASE_CREDS, DESTINATION_DATABASE_CREDS, TRANSFER_QUEUE_LIST

### Required Modules ###
This script requires a few non-standard modules to enable database connectivity. The following command should install the proper bits...
    
    >sudo pip install pymysql, psycopg2, psycopg2.extras, itertools
    
### Running the Transfer Script ###
Switch into the <strong>`src`</strong> directory and start the script from the module level

    >python eus_myemsl_sync


## Database Schema ##
this schema was coded against PostgreSQL 8.4+, but only uses fairly basic functionality, so it likely will work in older versions as well.

### Main Table Structures ###

* **`erica_proposal_xref`** - cross-references ERICA document IDs and EUS Proposal IDs
* **`institutions`** - List of institutions with past or present proposals in the EUS database
* **`eus_users`** - Cached copy of current EUS users
* **`institution_person_xref`** - Cross-reference between users and their home institutions
* **`instruments`** - Available instrumentation in EMSL
* **`proposal_info`** - Detailed information regarding EUS proposals (titles, abstracts, etc.)
* **`proposal_instrument_xref`** - Cross-reference between proposals and the EMSL instruments they involve
* **`proposal_participants`** - Cross-reference between EUS Users and their proposals

### Additional Tables (Currently Unused) ###

* **`journal_cache`** - Holding area for journal names and details
* **`erica_citations`** - Journal references for ERICA publications
* **`erica_contributors`** - Listing of ERICA authors and other contributing staff
* **`erica_keywords`** - Keywords trawled from ERICA publications
* **`erica_product_contributor_xref`** - Cross-reference between staff members and ERICA publications
