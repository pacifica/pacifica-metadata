#!/usr/bin/python
import pymysql
import psycopg2
import psycopg2.extras
import sys, traceback, pprint, logging
from sync_settings import SOURCE_DATABASE_CREDS, DESTINATION_DATABASE_CREDS, TRANSFER_QUEUE_LIST
from database_interfaces.eus_mysql import EUSDBInterface
from database_interfaces.myemsl_pg import MyEMSLPGInterface

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
# ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)



class EUSTransferSync():
  def __init__(self):
    
    source = SOURCE_DATABASE_CREDS
    dest = DESTINATION_DATABASE_CREDS
    
    self.source_db = EUSDBInterface(
      host=source.get('host'),
      database=source.get('database'),
      user=source.get('user'),
      password=source.get('password')    
    )
    self.dest_db = MyEMSLPGInterface(
      host=dest.get('host'),
      database=dest.get('database'),
      user=dest.get('user'),
      password=dest.get('password')
    )
  
  
  def start_transfer(self):
    table_list = TRANSFER_QUEUE_LIST
    for table in table_list.keys():
      #get the column list for the incoming table
      incoming_columns = self.source_db.get_field_names(table)
      logger.debug("Incoming Table Columns => {0}".format(incoming_columns))
      
      #get the existing records in the destination_table
      dest_table = table_list.get(table).get('destination_table')
      dest_schema = table_list.get(table).get('destination_schema')
      existing_records = self.dest_db.get_records(dest_table,dest_schema, incoming_columns)
      
      #now get the records for the incoming data
      incoming_records = self.source_db.get_records(table)
      
      # pprint.pprint(existing_records)
      # pprint.pprint(incoming_records)
      for row in existing_records:
        pprint.pprint(set(row.values()) - set(row.values()))
      exit()f
  
  
  '''
  Pass in...
    source and destination tables
    mapping relationship like {<source_column_name>:<dest_column_name>},
    filter collection like {<column_name>:<filter_value>}
  '''
  def transfer_table_contents(self, source_table, destination_table, mapping_relation = None, filter_collection = None):
    pass    
    
        

'''
Run this as unit testing code
'''
if __name__ == '__main__':
  logger.setLevel(logging.DEBUG)
  sync = EUSTransferSync()
  # source_table = 'MYEMSL_EUS_USERS'
  # destination_table = 'eus_users'
  # sync.transfer_table_contents(source_table, destination_table)
  sync.start_transfer()