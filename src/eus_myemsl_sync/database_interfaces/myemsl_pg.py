# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import sys,traceback,pprint,logging,itertools

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
# ch.setLevel(logging.ERROR)
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
			
			
			
	def get_field_names(self,table_name):
	
			select_sql = '''
	SELECT * FROM {0} LIMIT 1
'''.format(table_name)

			col_list = []
	
			cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			cur.execute(select_sql)
			col_list = [desc[0] for desc in cur.description if desc[0] not in ['created','updated','deleted']]
				
			return col_list
			
			
			
	def get_record_collection(self,table_list):
		results = {}
		for table_name in table_list.keys():
			where_clause = table_list.get(table_name).get('where_clause')
			results[table_name] = self.get_records(table_name,None,where_clause)
			
		return results
	
	
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
		
	
	def insert_records(self, table_name, insert_data, field_names=None):
		def split_seq(iterable, size):
			it = iter(iterable)
			item = list(itertools.islice(it, size))
			while item:
				yield item
				item = list(itertools.islice(it, size))

		cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		if field_names is None:
			field_names = self.get_field_names(table_name)
		# values = insert_data.values()
		
		split_inserts = list(split_seq(insert_data,500))
		
		for item in split_inserts:
			insert_sql = '''
			INSERT INTO {0} ({1}) VALUES {2}
			'''.format(table_name, ",".join(field_names), ",".join(['%s'] * len(insert_data)))
			
			cur.execute(insert_sql, insert_data)
		rowcount = cur.rowcount
		self.db_conn.commit()
		cur.close()
		
		return rowcount
			

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

	insert_data = [("49067","PREMIER CAT - Using Dynamic TEM to Study the Nucleation and Growth of Organic Semiconductor Nanostructures","The in situ growth of organic crystalline nanostructures in solution will be examined by dynamic TEM to understand the growth mechanism of these unusual structures. This understanding will aid in the development of new materials with novel geometries for applications in light sensing devices for electronics and energy production. Using the liquid flow holder available at EMSL we will react two heated solutions and observe the growth phenomenon by the successive image capturing capabilities of the dynamic TEM. The dynamic TEM will enable us to avoid electron beam damage of these organic materials.","Other","4","PREMIER CAT","12/03/2015 17:19:27","12/17/2015","01/04/2016","09/30/2016","12/17/2015 14:04:34"),("49197","Atom-probe tomography of epitaxial complex oxide nanocomposites","The goal of this proposal is to study the interfacial composition of between immiscible complex oxides and spinel oxide nanostructures using atom probe tomography in order to understanding the chemical interactions that drive phase segregation.  To date, no systematic study of complex oxide materials using atom probe tomography has been reported.  The results from atom probe tomography will open new pathways for future research related to solid oxide fuel cells and solar driven energy applications such as artificial photosynthesis at PNNL and enhance the understanding of the thermodynamics and kinetics that drive phase segregation in the materials.","Energy Materials and Processes","2","EMSL","11/30/2015 12:35:26","12/17/2015","12/17/2015","09/30/2016","12/17/2015 12:24:03"),("49196","FT ICRMS analysis to assess the molecular-level composition of dissolved organic nitrogen in the runoff and surface water in the Indian River Lagoon, South Florida","We propose to utilize EMSL’s ultra-high resolution mass spectrometry to determine the composition of dissolved organic N from runoff water and surface water of Indian River Lagoon. It is important to quantify and qualify dynamics of dissolved organic nitrogen, which remains poorly represented in in existing models for prediction of N fate and transport in surface waters of this area. Specifically, this experiment is designed to test the influence of rainfall, temperature and fertilization on the dynamics of dissolved organic nitrogen in runoff and surface water samples in the Indian River Lagoon. Integration of this information will help to develop best management practices (BMPs) in south Florida.","Terrestrial and Subsurface Ecosystems","1","RAPID","11/23/2015 14:08:37","12/16/2015","01/26/2016","02/24/2016","12/16/2015 14:23:09"),("49193","Understanding nanoscale composition and structure of U-10Mo alloys.","PNNL as a part of the Global Threat Reduction Initiative (GTRI) Convert program is working on converting the high enriched uranium (HEU) fuel currently used in civilian research and test reactors to low enriched uranium fuels (LEU) to permanently secures the site by removing the threat posed by continued HEU operations. Several experimental programs aimed at developing of LEU fuels are in progress at PNNL in collaboration with other national laboratories and require detailed characterization of the microstructure of these fuels as a function of various processing methods and composition of raw materials. The materials consist primarily of cast or heat treated or rolled depleted uranium-10Mo alloy plates. The primary microstructure of these plates consists of U-Mo BCC matrix with other impurity phases like Uranium carbides, MoSi2 or oxide precipitates. In order to ensure the quality of the U-10Mo fuel plates as a function of different processing parameters and composition of raw materials, detailed microstructural characterization of the final U-10Mo alloys needs to be conducted using electron microscopy, xray diffraction and atom probe tomography. This EMSL proposal is submitted to obtain access to EMSL instrumentation in EMSL radiochemistry annex and in EMSL building for this nationally and globally significant project.   ","Energy Materials and Processes","2","EMSL","11/17/2015 14:33:15","12/04/2015","12/04/2015","09/30/2016","12/04/2015 13:29:46"),("49191","ATOM PROBE TOMOGRAPHY (APT) OF HEAVY-METAL RICH BIOMATERIALS FROM SOIL ARTHROPODS","The jaws, leg claws, stings and other ?tools? of a large fraction of arthropods, some worms and members of other phyla, contain extraordinary amounts of heavy metals or bromine (e.g. Zn, Mn, Fe, Cu, and Br), which we term heavy-element biomaterials (HEBs).  Although the concentrations reach 25 of dry mass, these materials do not contain an ordered biomineral, like calcified tissues. In fact, X-ray absorption spectroscopy suggests that, in the Zn-version of these biomaterials, the spacing between even the closest Zn atoms is irregular. We propose to use APT, 67Zn NMR and possibly other techniques at EMSL to better understand the structure of several types of these materials. In particular, we will test the hypothesis that Zn is bound to three hydroxides and either a fourth hydroxide or a histidine imidazole nitrogen, in nanometer-scale inclusions. And we will investigate whether other metals used in HEBs are also bound in nanoclusters.","Terrestrial and Subsurface Ecosystems","1","PROPRIETARY_PUBLIC","11/13/2015 15:40:21","12/09/2015","12/09/2015","09/30/2016","12/09/2015 10:27:34"),("49189","NMR based metabolomics of Apis mellifera, the honeybee, under sub-lethal stress from the neonicotinoid pesticide, Imidacloprid","Insect pollinators are important components of the environment and agriculture. Recent declines in pollinators, such as the honey bee, could impact global food production and ecosystem stability.  The use of neonicotinoid insecticides in agricultural, industrial and residential settings has been proposed as a contributor to the decline of insect pollinators.  We propose the application of quantitative NMR based metabolomics to assess the metabolic responses of the honey bee to sublethal doses of the neonicotinoid insecticide, imidacloprid","Biosystems Dynamics and Design","3","EMSL","11/11/2015 11:20:25","11/23/2015","11/23/2015","09/30/2016","11/23/2015 09:23:32")]

	i.insert_records('proposal_info.proposal_info',insert_data)

	# table_list = {
	# 	'MYEMSL_EUS_USERS' : {"where_clause":"last_change_date > '2015-12-01'"},
	# 	'MYEMSL_INSTITUTION_PERSON_XREF' : {"where_clause" : "1=1"},
	# 	'MYEMSL_INSTITUTIONS' : {"where_clause" : "1=1"},
	# 	'MYEMSL_INSTRUMENTS' : {"where_clause" : "1=1"}
	# }
	# results = i.get_record_collection(table_list)
	# pprint.pprint(results)

