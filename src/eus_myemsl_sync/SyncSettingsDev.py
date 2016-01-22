SOURCE_DATABASE_CREDS = {
	'host':'eusi.emsl.pnl.gov',
	'database':'ERSUPPLAY',
	'user':'ersup_play',
	'password':'play'
}
DESTINATION_DATABASE_CREDS = {
	'host':'localhost',
	'database':'myemsl_metadata',
	'schema':'eus_new',
	'user':'metadata_admins',
	'password':'md4real'
}

TRANSFER_QUEUE_LIST = {
	 'MYEMSL_EUS_USERS' : {
	 	'destination_table' : 'users',
	 	'destination_schema' : 'eus_new',
	 	'order_by_clause' : 'person_id'
	 },
	 'MYEMSL_INSTITUTIONS' : {
	 	'destination_table' : 'institutions',
	 	'destination_schema' : 'eus_new',
	 	'order_by_clause' : 'institution_id'
	 },
	'MYEMSL_INSTRUMENTS' : {
		'destination_table' : 'instruments',
		'destination_schema' : 'eus_new',
		'order_by_clause' : 'instrument_id'
	},
   'MYEMSL_eus_new' : {
   	'destination_table' : 'eus_new',
   	'destination_schema' : 'eus_new',
   	'order_by_clause' : 'proposal_id'
   },
   'MYEMSL_INSTITUTION_PERSON_XREF' : {
   	'destination_table' : 'institution_person_xref',
   	'destination_schema' : 'eus_new',
   	'order_by_clause' : 'person_id'
   },
   'MYEMSL_PROPOSAL_INSTRUMENT_XREF' : {
   	'destination_table' : 'proposal_instrument_xref',
   	'destination_schema' : 'eus_new',
   	'order_by_clause' : 'instrument_id,proposal_id'
   },
   'MYEMSL_PROPOSAL_PARTICIPANTS' : {
   	'destination_table' : 'proposal_participants',
   	'destination_schema' : 'eus_new',
   	'order_by_clause' : 'proposal_id,person_id'
    },
    'MYEMSL_ERICA_PROPOSAL_XREF' : {
	   'destination_table' : 'erica_proposal_xref',
	   'destination_schema' : 'eus_new',
	   'order_by_clause' : 'erica_product_id'
    }
 }