#!/usr/bin/python
import pprint, logging
from database_interfaces.MySQLDBInterface import MySQLDBInterface
from database_interfaces.PGDBInterface import PGDBInterface

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.setLevel(logging.ERROR)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)



from SyncSettingsDev import SOURCE_DATABASE_CREDS, DESTINATION_DATABASE_CREDS, TRANSFER_QUEUE_LIST



class EUSTransferSync():
  def __init__(self):
    
  
    source = SOURCE_DATABASE_CREDS
    dest = DESTINATION_DATABASE_CREDS
    

    self.source_db = MySQLDBInterface(
      host=source.get('host'),
      database=source.get('database'),
      user=source.get('user'),
      password=source.get('password')    
    )
  
    self.dest_db = PGDBInterface(
      host=dest.get('host'),
      database=dest.get('database'),
      user=dest.get('user'),
      password=dest.get('password')
    )      
    
    self.dest_schema = dest.get('schema')    
  
  
  def start_transfer(self, force=False):
    table_list = TRANSFER_QUEUE_LIST
    for table in table_list.keys():
      #get the existing records in the destination_table
      dest_table = table_list.get(table).get('destination_table')
      dest_schema = table_list.get(table).get('destination_schema')

      #get the last updated timestamp
      last_update = self.dest_db.get_last_update_time(dest_schema,dest_table)
      if last_update is not None:
        logger.debug("{0} was last updated on {1} at {2}".format(dest_table, last_update.strftime('%m/%d/%Y'),last_update.strftime('%H:%M:%S')))
      else:
        logger.debug("{0} has no last updated time".format(dest_table))
      
      #get the column list for the source table
      incoming_columns = self.source_db.get_field_names(table)
      logger.debug("Source Table Columns => {0}".format(incoming_columns))
      
      has_change_date = True if 'last_change_date' in incoming_columns else False
                  
      #get the column list for the destination table
      dest_columns = self.dest_db.get_field_names(dest_schema,dest_table)
      logger.debug("Destination Table Columns => {0}".format(dest_columns))
      
      #get the primary keys for the destination table
      dest_pk_list = self.dest_db.get_primary_keys(dest_schema, dest_table)
            
      #now get the records for the incoming data
      logger.debug("last_update_time => {0}".format(last_update))
      if has_change_date:
        where_clause = "last_change_date > '{0}'".format(last_update.strftime('%Y-%m-%d %H:%M:%S')) if force == False else None
      else:
        where_clause = None
        
      incoming_records = self.source_db.get_records(table,incoming_columns,where_clause)
      
    
      where_list = ["{0} = %s".format(col) for col in dest_pk_list]
      
      replaced_row_count = 0
      inserted_row_count = 0
      
      for rec in incoming_records:
        #logger.debug("record => {0}".format(rec))
        where_values = []
        #build the where clause for exact matches
        for col in dest_pk_list:
          test_value = rec.get(col)
          if(col == 'last_change_date'):
            test_value = test_value.strftime('%Y-%m-%d %H:%M:%S')
          where_values.append(test_value)
        
        
        matching_record = self.dest_db.get_matching_record(dest_table, dest_schema, incoming_columns, where_list, where_values)
        if matching_record is not None:
          matching_record = matching_record.pop()
          #found a matching primary key, but the values probably have changed. Strike our record and replace it with the new one
          if self.record_has_changed(rec, matching_record):
            affected_rows = self.dest_db.replace_record(dest_table, dest_schema, where_list, where_values, rec)
            replaced_row_count += affected_rows
        else:
          insert_values = [tuple(rec.values())]
          affected_rows = self.dest_db.insert_records(dest_table, dest_schema, insert_values, rec.keys())   
          inserted_row_count += affected_rows
          
      logger.info("Replaced {0} entries, added {1} entries to table {2}".format(replaced_row_count,inserted_row_count,dest_table))    
    
    
  def record_has_changed(self, source_record, dest_record):
    result = False
    for column in source_record.keys():
      source_value = source_record.get(column)
      column = column.encode('ascii','ignore')
      dest_value = dest_record.get(column)
      if dest_value != source_value:
        result = True
        break
    return result
        

'''
Run this as unit testing code
'''
if __name__ == '__main__':
  logger.setLevel(logging.DEBUG)
  sync = EUSTransferSync()
  table_list = TRANSFER_QUEUE_LIST
    
  # for table in table_list.keys():
  #   dest_table = table_list.get(table).get('destination_table')
  #   dest_schema = table_list.get(table).get('destination_schema')
  #   pk_list = sync.dest_db.get_primary_keys(dest_schema, dest_table)
  #   
  #   logger.debug("Table => {0} | Primary Keys => {1}".format(dest_table,pk_list))
  
  
  # source_table = 'MYEMSL_EUS_USERS'
  # destination_table = 'eus_users'
  # sync.transfer_table_contents(source_table, destination_table)
  #sync.start_transfer()