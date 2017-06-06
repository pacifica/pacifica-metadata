"""CherryPy Status Metadata object class."""
import datetime
import pytz
from dateutil.parser import parse
from cherrypy import tools, request
from peewee import Expression, OP
from metadata.rest.reporting_queries.query_base import QueryBase
from metadata.orm import Transactions, Files
from metadata.orm.base import db_connection_decorator


# pylint: disable=too-few-public-methods
class SummarizeByDate(QueryBase):
    """Retrieves a list of all transactions matching the search criteria."""

    exposed = True

    @staticmethod
    def _search_by_dates(object_type, object_id_list, start_date, end_date, time_basis):
        time_column_name = QueryBase.time_basis_mappings.get(time_basis)
        object_type_column_name = QueryBase.object_type_mappings.get(object_type)

        if time_basis == 'submitted':
            time_column = getattr(Transactions, time_column_name)
        else:
            time_column = getattr(Files, time_column_name)
        object_type_column = getattr(Transactions, object_type_column_name)

        where_clause = Expression(time_column, OP.GTE, start_date)
        where_clause &= Expression(time_column, OP.LTE, end_date)
        where_clause &= (object_type_column << object_id_list)
        query = Files().select(
            Files.id, time_column.alias('filedate'), Files.size, Files.transaction
        ).join(Transactions)

        query = query.where(where_clause).order_by(time_column).naive()

        results = {
            'day_graph': {
                'by_date': {
                    'available_dates': {},
                    'file_count': {},
                    'file_volume': {},
                    'transactions': {},
                    'file_volume_array': {},
                    'transaction_count_array': {}
                }
            },
            'summary_totals': {
                'upload_stats': {
                    'proposal': {},
                    'instrument': {},
                    'user': {}
                },
                'total_file_count': 0,
                'total_size_bytes': 0,
                'total_size_string': ''
            },
            'transaction_info': {
                'transaction': {},
                'proposal': {},
                'instrument': {},
                'user': {}
            }
        }

        raw_results = {d['id']: d for d in query.dicts()}

        for item in query:
            results['day_graph']['by_date'] = SummarizeByDate._summarize_by_date(
                results['day_graph']['by_date'], item, raw_results)

            results['transaction_info']['transaction'][item.transaction.id] = item.transaction.to_hash()
            results['transaction_info']['proposal'][item.transaction.proposal.id] = item.transaction.proposal.title
            results['transaction_info']['instrument'][item.transaction.instrument.id] = item.transaction.instrument.name
            results['transaction_info']['user'][item.transaction.submitter.id] = '{0} {1}'.format(
                item.transaction.submitter.first_name, item.transaction.submitter.last_name)

            SummarizeByDate._summarize_upload_stats(results['summary_totals']['upload_stats'], item)

            results['summary_totals']['total_file_count'] += 1
            results['summary_totals']['total_size_bytes'] += item.size

        return results

    @staticmethod
    def _summarize_upload_stats(upload_stats_block, item):
        if item.transaction.proposal.id not in upload_stats_block['proposal'].keys():
            upload_stats_block['proposal'][item.transaction.proposal.id] = 0
        upload_stats_block['proposal'][item.transaction.proposal.id] += 1

        if item.transaction.instrument.id not in upload_stats_block['instrument'].keys():
            upload_stats_block['instrument'][item.transaction.instrument.id] = 0
        upload_stats_block['instrument'][item.transaction.instrument.id] += 1

        if item.transaction.submitter.id not in upload_stats_block['user'].keys():
            upload_stats_block['user'][item.transaction.submitter.id] = 0
        upload_stats_block['user'][item.transaction.submitter.id] += 1

        return upload_stats_block

    @staticmethod
    def _summarize_by_date(summary_block, item, raw_results):
        current_day = SummarizeByDate._utc_to_local(raw_results[item.id]['filedate']).date()
        current_day = current_day.strftime('%Y-%m-%d')
        if current_day not in summary_block['file_count'].keys():
            summary_block['file_count'][current_day] = 0
        if current_day not in summary_block['file_volume'].keys():
            summary_block['file_volume'][current_day] = 0
        if current_day not in summary_block['transactions'].keys():
            summary_block['transactions'][current_day] = []
        summary_block['file_count'][current_day] += 1
        summary_block['file_volume'][current_day] += item.size
        if item.transaction_id not in summary_block['transactions'][current_day]:
            summary_block['transactions'][current_day].append(item.transaction.id)

        return summary_block

    @staticmethod
    def _local_to_utc(local_datetime_obj):
        utc_datetime_obj = QueryBase.local_timezone.localize(local_datetime_obj)
        utc_datetime_obj.astimezone(pytz.timezone('UTC'))
        return utc_datetime_obj

    @staticmethod
    def _utc_to_local(utc_datetime_obj):
        local_datetime_obj = pytz.timezone('UTC').localize(utc_datetime_obj)
        local_datetime_obj.astimezone(QueryBase.local_timezone)
        return local_datetime_obj

    @staticmethod
    def _canonicalize_dates(start_date, end_date):
        try:
            start_date_obj = SummarizeByDate._local_to_utc(parse(start_date))
        except ValueError:
            start_date_obj = SummarizeByDate._local_to_utc(parse('1997-01-01'))
        try:
            end_date_obj = SummarizeByDate._local_to_utc(parse(end_date))
        except ValueError:
            end_date_obj = SummarizeByDate._local_to_utc(datetime.datetime.now())

        return start_date_obj.isoformat(), end_date_obj.isoformat()

    # Cherrypy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_in()
    @tools.json_out()
    @db_connection_decorator
    def POST(time_basis=None, object_type=None, start_date=None, end_date=None):
        """Return summaryinfo for a given object type/id/time range combo."""
        # check time basis validity
        time_basis_list = {'creat': 'created', 'modif': 'modified', 'submi': 'submitted'}
        if time_basis[0:5] not in time_basis_list.keys() or time_basis is None:
            time_basis = 'modified'
        else:
            time_basis = time_basis_list[time_basis[0:5]]

        object_type_list = ['instrument', 'proposal', 'user']
        if object_type not in object_type_list or object_type is None:
            object_type = 'instrument'

        # check start/end date validity
        start_date, end_date = SummarizeByDate._canonicalize_dates(start_date, end_date)

        return SummarizeByDate._search_by_dates(
            object_type, request.json,
            start_date, end_date, time_basis)
