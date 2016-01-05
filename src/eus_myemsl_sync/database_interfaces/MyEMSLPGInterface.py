# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import datetime as dt
import traceback,logging,itertools

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class MyEMSLPGInterface(object):
	'''
	class documentation here
	'''

	def __init__(self,
							 host='localhost',
							 database='default',
							 user=None,
							 password=None):

		self.debug_on = True if logger.getEffectiveLevel() == logging.DEBUG else False

		self.database = database
		
		psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
		psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

		connection_parameters = {'host' : host,
														 'dbname' : database,
														 'user' : user,
														 'password' : password}
		self.db_conn = self.db_setup(connection_parameters)




	def db_setup(self, conn_params):
		connection_collection = ["{0}='{1}'".format(param,conn_params.get(param)) for param in conn_params.keys()]
		connection_string = " ".join(connection_collection)
		logger.debug("connection_string => {0}".format(connection_string))
		try:
			conn = psycopg2.connect(connection_string)
			logger.debug("Sucessfully connected to '{0}' database on host {1}".format(conn_params.get('dbname'),conn_params.get('host')))
			return conn
		except:
			logger.error(traceback.format_exc())
			# traceback.print_exc()
			
			
			
	
	
	def get_field_names(self,schema_name,table_name):
	
			select_sql = '''
	SELECT * FROM {0}.{1} LIMIT 1
'''.format(schema_name,table_name)

			col_list = []
	
			cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			cur.execute(select_sql)
			col_list = [desc[0].encode('ascii', 'ignore') for desc in cur.description if desc[0] not in ['created','updated','deleted']]
				
			return col_list
			
			
	
	
	def get_primary_keys(self,schema_name,table_name):
		select_sql = '''
SELECT column_name
FROM information_schema.table_constraints
		 JOIN information_schema.key_column_usage
				 USING (constraint_catalog, constraint_schema, constraint_name,
								table_catalog, table_schema, table_name)
WHERE constraint_type = 'PRIMARY KEY'
	AND (table_schema, table_name) = ('{0}', '{1}')
ORDER BY ordinal_position;		
		'''.format(schema_name,table_name)
		pk_list = []
		cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(select_sql)
		results = cur.fetchall()
		pk_list = [row.get('column_name').encode('ascii','ignore') for row in results]
		
		return pk_list
			
			
			
			
	
	def get_matching_record(self,table,schema,field_collection,where_list,where_values):
		fields = ",".join(field_collection) if field_collection is not None else '*'
		select_sql = "SELECT {0} FROM {1}.{2}".format(fields,schema,table)
		cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		#if where_list is not None and where_values is not None:
		where_string = " AND ".join(where_list)
		where_values = tuple(where_values)
		select_sql += " WHERE {0}".format(where_string)
		logger.debug("Current Match Check Query = {0}".format(cur.mogrify(select_sql,where_values)))
		cur.execute(select_sql,where_values)
		if cur.rowcount > 0:
			return cur.fetchall()
		else:
			return None
			
	
	
	# def remove_record(self,table,schema,where_columns,where_values):
	# 	cur = self.db_conn.cursor()
	# 	where_list = ["{0} = %s".format(col) for col in where_columns]
	# 	where_string = " AND ".join(where_list)
	# 	delete_sql = "DELETE FROM {0}.{1} WHERE {2}".format(schema,table,where_string)
	# 	try:
	# 		cur.execute(delete_sql,where_values)
	# 		self.db_conn.commit()
	# 	except:
	# 		self.db_conn.rollback()
	# 		logger.error("Could not delete row represented by {0} and {1}".format(where_columns,where_values))
	# 	return cur.rowcount
		
		
	
	
	
	def replace_record(self,table,schema,where_list,where_values,new_record):
		cur = self.db_conn.cursor()
		# where_list = ["{0} = %s".format(col) for col in where_columns]

		where_string = " AND ".join(where_list)
		delete_sql = "DELETE FROM {0}.{1} WHERE {2}".format(schema,table,where_string)
		insert_sql = "INSERT INTO {0}.{1} ({2}) VALUES ({3})".format(schema,table,','.join(new_record.keys()), ",".join(['%s'] * len(new_record.keys())))
		try:
			cur.execute(delete_sql,where_values)
			cur.execute(insert_sql,new_record.values())
			self.db_conn.commit()
		except:
			self.db_conn.rollback()
			logger.debug("delete sql => {0}, where_values => {1}".format(delete_sql,where_values))
			logger.debug("insert sql => {0}, new_values => {1}".format(insert_sql,new_record.values()))
			logger.error("Could not delete row represented by {0} and {1}".format(where_list,where_values))
			logger.error(traceback.format_exc())
		return cur.rowcount
		
	
	
	
	
	def get_records(self,table,schema,field_collection=None,whereclause=None,orderbyclause=None):
		# if field_collection is None:
		# 	field_collection = self.get_field_names(table)
		# field_collection = field_collection if not None else self.get_field_names(table)
		# logger.debug("field collection => {0}".format(",".join(field_collection)))
		
	
		fields = ",".join(field_collection) if field_collection is not None else '*'
		select_sql = "SELECT {0} FROM {1}.{2}".format(fields,schema,table)
		if whereclause is not None:
			select_sql += " WHERE {0}".format(whereclause)
		if orderbyclause is not None:
			select_sql += " ORDER BY {0}".format(orderbyclause)
		if logger.getEffectiveLevel() == logging.DEBUG:
			select_sql += " LIMIT 100"
		logger.debug("Current Query => {0}".format(select_sql))
		cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		psycopg2.extensions.register_type(psycopg2.extensions.UNICODE,cur)
		psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY,cur)		
		cur.execute(select_sql)
		results = cur.fetchall()
		cur.close()
		logger.debug("Pulled {0} records from {1}".format(cur.rowcount,table))
		return results
		
	
	
	
	
	def insert_records(self, table_name, schema_name, insert_data, field_names=None):
		def split_seq(iterable, size):
			it = iter(iterable)
			item = list(itertools.islice(it, size))
			while item:
				yield item
				item = list(itertools.islice(it, size))

		cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		if field_names is None:
			field_names = self.get_field_names(schema_name, table_name)
		# values = insert_data.values()
		
		split_inserts = list(split_seq(insert_data,500))
		
		for item in split_inserts:
			insert_sql = '''
			INSERT INTO {0}.{1} ({2}) VALUES {3}
			'''.format(schema_name, table_name, ",".join(field_names), ",".join(['%s'] * len(insert_data)))
			logger.debug("Current Insert Query => {0}".format(insert_sql))
			cur.execute(insert_sql, insert_data)
		rowcount = cur.rowcount
		self.db_conn.commit()
		cur.close()
		
		return rowcount
		
	
	
	def get_last_update_time(self,schema_name,table_name):
		cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		select_sql = "SELECT last_change_date::timestamp as updated from {0}.{1} ORDER BY last_change_date desc LIMIT 1".format(schema_name,table_name)
		cur.execute(select_sql)
		if cur.rowcount > 0:
			results = cur.fetchone()
			last_update = results.get('updated')
		else:
			last_update = dt.datetime(1983,1,1)
			
		return last_update
			

'''
Run this as unit testing code
'''
if __name__ == '__main__':
	logger.setLevel(logging.DEBUG)
	i = MyEMSLPGInterface(host='localhost',
										 database='myemsl_biblio_database', user='metadata_admins',
										 password='md4real')

	# field_names = i.get_field_names('proposal_info.proposal_info')
	# pprint.pprint(field_names)
	# 
	# 
	# records = i.get_records('proposal_info.proposal_info',None)
	# pprint.pprint(records)

	# insert_data = [("49067","PREMIER CAT - Using Dynamic TEM to Study the Nucleation and Growth of Organic Semiconductor Nanostructures","The in situ growth of organic crystalline nanostructures in solution will be examined by dynamic TEM to understand the growth mechanism of these unusual structures. This understanding will aid in the development of new materials with novel geometries for applications in light sensing devices for electronics and energy production. Using the liquid flow holder available at EMSL we will react two heated solutions and observe the growth phenomenon by the successive image capturing capabilities of the dynamic TEM. The dynamic TEM will enable us to avoid electron beam damage of these organic materials.","Other","4","PREMIER CAT","12/03/2015 17:19:27","12/17/2015","01/04/2016","09/30/2016","12/17/2015 14:04:34"),("49197","Atom-probe tomography of epitaxial complex oxide nanocomposites","The goal of this proposal is to study the interfacial composition of between immiscible complex oxides and spinel oxide nanostructures using atom probe tomography in order to understanding the chemical interactions that drive phase segregation.  To date, no systematic study of complex oxide materials using atom probe tomography has been reported.  The results from atom probe tomography will open new pathways for future research related to solid oxide fuel cells and solar driven energy applications such as artificial photosynthesis at PNNL and enhance the understanding of the thermodynamics and kinetics that drive phase segregation in the materials.","Energy Materials and Processes","2","EMSL","11/30/2015 12:35:26","12/17/2015","12/17/2015","09/30/2016","12/17/2015 12:24:03"),("49196","FT ICRMS analysis to assess the molecular-level composition of dissolved organic nitrogen in the runoff and surface water in the Indian River Lagoon, South Florida","We propose to utilize EMSL’s ultra-high resolution mass spectrometry to determine the composition of dissolved organic N from runoff water and surface water of Indian River Lagoon. It is important to quantify and qualify dynamics of dissolved organic nitrogen, which remains poorly represented in in existing models for prediction of N fate and transport in surface waters of this area. Specifically, this experiment is designed to test the influence of rainfall, temperature and fertilization on the dynamics of dissolved organic nitrogen in runoff and surface water samples in the Indian River Lagoon. Integration of this information will help to develop best management practices (BMPs) in south Florida.","Terrestrial and Subsurface Ecosystems","1","RAPID","11/23/2015 14:08:37","12/16/2015","01/26/2016","02/24/2016","12/16/2015 14:23:09")]
	# 
	# #i.insert_records('proposal_info.proposal_info',insert_data)
	

	#i.get_primary_keys('proposal_info', 'institutions')

	# table_list = {
	# 	'MYEMSL_EUS_USERS' : {"where_clause":"last_change_date > '2015-12-01'"},
	# 	'MYEMSL_INSTITUTION_PERSON_XREF' : {"where_clause" : "1=1"},
	# 	'MYEMSL_INSTITUTIONS' : {"where_clause" : "1=1"},
	# 	'MYEMSL_INSTRUMENTS' : {"where_clause" : "1=1"}
	# }
	# results = i.get_record_collection(table_list)
	# pprint.pprint(results)

