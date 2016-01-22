#!/usr/bin/python
import pymysql
import sys,traceback,pprint,logging

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
#logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class MySQLDBInterface(object):
	'''
	This is the interface to the MySQL database that EUS is using to store their
	proposal and user metadata.
	'''
	
	def __init__(self,host='localhost',database='default',user=None,password=None):			 
		self.debug_on = True if logger.getEffectiveLevel() == logging.DEBUG else False
							 
		self.database = database
		
		connection_parameters = {'host' : host,
														 'database' : database,
														 'user' : user,
														 'password' : password}
		self.db_conn = self.db_setup(connection_parameters)
		
	
		
		
	def db_setup(self, conn_params):
		try:
			conn = pymysql.connect(host=conn_params.get('host'),
			 											 user=conn_params.get('user'),
			 											 password=conn_params.get('password'),
			 											 db=conn_params.get('database'),
			 											 charset='utf8',
			 											 cursorclass=pymysql.cursors.DictCursor)
			logger.debug("Sucessfully connected to {0} database on host {1}".format(conn_params.get('database'),conn_params.get('host')))
			return conn
		except:
			logger.error(traceback.format_exc())
			# traceback.print_exc()
			
			
				
	
	def get_records(self,table,field_collection=None,whereclause=None,orderbyclause=None):
		if field_collection is None:
			field_collection = self.get_field_names(table)
		logger.debug("field collection => {0}".format(",".join(field_collection)))
		cleaned_field_collection = ["{0} as {1}".format(x,x.lower()) for x in field_collection] if field_collection is not None else ['*']
		logger.debug("cleaned field collection => {0}".format(",".join(cleaned_field_collection)))

		fields = ",".join(cleaned_field_collection) if field_collection is not None else '*'
		#print "fields => {0}".format(fields)
		select_sql = "SELECT {0} FROM {1}".format(fields,table)
		if whereclause is not None:
			select_sql += " WHERE {0}".format(whereclause)
		if orderbyclause is not None:
			select_sql += " ORDER BY {0}".format(orderbyclause)
		# if logger.getEffectiveLevel() == logging.DEBUG:
		# 	select_sql += " LIMIT 100"
		logger.debug("Current Query => {0}".format(select_sql))
		with self.db_conn.cursor() as cur:
			try:
				cur.execute(select_sql)
				logger.debug("Pulled {0} records from {1}".format(cur.rowcount,table))
			except:
				print select_sql
				logger.error(traceback.format_exc())

		return cur.fetchall()
				
				
	def get_field_names(self,table_name, lower_case=True):
		
		select_sql = '''
SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = %s AND
	TABLE_NAME = %s
		'''
		
		col_list = []
		logger.debug("column select sql => {0}".format(select_sql))
		logger.debug("Grabbing column names => {0}".format(select_sql))
		
		with self.db_conn.cursor() as cur:
			cur.execute(select_sql,(self.database,table_name))
			for row in cur.fetchall():
				col_name = row.values().pop().encode('ascii', 'ignore')
				if lower_case:
					col_name = col_name.lower()
				col_list.append(col_name)
				
		return col_list
			
'''
Run this as unit testing code
'''
if __name__ == '__main__':
	logger.setLevel(logging.DEBUG)
	i = EUSDBInterface(host='eusi.emsl.pnl.gov',
										 database='ERSUPPLAY', user='ersup_play',
										 password='play')
										 
	# i.get_field_names('MYEMSL_EUS_USERS')
										 
	# i.get_records('MYEMSL_EUS_USERS',
	# 							['NETWORK_ID','PERSON_ID','first_name'],
	# 							"last_change_date > '2015-12-01'",
	# 							"PERSON_ID")
	
	# table_list = {
	# 	'MYEMSL_EUS_USERS' : {"where_clause":"last_change_date > '2015-12-01'"},
	# 	'MYEMSL_INSTITUTION_PERSON_XREF' : {"where_clause" : "1=1"},
	# 	'MYEMSL_INSTITUTIONS' : {"where_clause" : "1=1"},
	# 	'MYEMSL_INSTRUMENTS' : {"where_clause" : "1=1"}
	# }
	# results = i.get_record_collection(table_list)
	# pprint.pprint(results)
	
