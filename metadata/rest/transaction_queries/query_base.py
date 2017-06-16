"""CherryPy Status Metadata proposalinfo base class."""
from peewee import DoesNotExist, fn, JOIN
from metadata.orm import TransactionKeyValue, Keys, Values
from metadata.orm import Files, FileKeyValue, Transactions
from metadata.orm import Users, Instruments, Proposals
from cherrypy import HTTPError


# pylint: disable=too-few-public-methods
class QueryBase(object):
    """Retrieves a set of proposals for a given keyword set."""

    @staticmethod
    def _get_transaction_key_values(transaction_id):
        where_clause = TransactionKeyValue().where_clause(
            {'transaction_id': transaction_id}
        )
        tkv_list = (TransactionKeyValue
                    .select(Keys.key, Values.value)
                    .join(Keys, on=(Keys.id == TransactionKeyValue.key))
                    .join(Values, on=(Values.id == TransactionKeyValue.value))
                    .where(where_clause)
                    .order_by(TransactionKeyValue.key)
                    .dicts())

        return [tkv for tkv in tkv_list]

    @staticmethod
    def _get_file_list(transaction_id):
        where_clause = Files().where_clause({'transaction_id': transaction_id})
        files_list = (Files
                      .select()
                      .where(where_clause)
                      .order_by(Files.name))

        return {f.id: f.to_hash() for f in files_list}

    @staticmethod
    def _get_transaction_info_block(transaction_id, option='details'):
        try:
            transaction_entry = Transactions()
            where_clause = transaction_entry.where_clause(
                {'_id': transaction_id})
            transaction_info = (Transactions
                                .select()
                                .where(where_clause)
                                .get())

            transaction_entry = transaction_info.to_hash()
        except DoesNotExist:
            message = 'No Transaction with an ID of {0} was found'.format(
                transaction_id)
            raise HTTPError('404 Not Found', message)

        transaction_metadata = QueryBase._get_base_transaction_metadata(
            transaction_entry, option)

        kv_list = {}
        kvs = QueryBase._get_transaction_key_values(transaction_id)
        for key_value in kvs:
            kv_list.update({key_value['key']: key_value['value']})

        transaction_entry.update(transaction_metadata)
        transaction_entry['key_values'] = kv_list

        return transaction_entry

    @staticmethod
    def _get_transaction_info_blocks(transaction_list, option='details'):
        transactions = (Transactions
                        .select(
                            Transactions,
                            fn.Sum(Files.size).alias('file_size_bytes'),
                            fn.Count(Files.id).alias('file_count')
                        )
                        .join(Files, JOIN.LEFT_OUTER)
                        .group_by(Transactions)
                        .where(Transactions.id << transaction_list))

        transaction_results = {'transactions': {}, 'times': {}}

        for trans in transactions:
            kv_list = {}
            entry = trans.to_hash()
            metadata = QueryBase._get_base_transaction_metadata(entry, option)
            transaction = {}
            kvs = QueryBase._get_transaction_key_values(trans.id)
            for key_value in kvs:
                kv_list.update({key_value['key']: key_value['value']})
            transaction['file_size_bytes'] = int(
                trans.file_size_bytes) if trans.file_size_bytes is not None else 0
            transaction['file_count'] = int(
                trans.file_count) if trans.file_count is not None else 0
            transaction['status'] = {
                'trans_id': trans.id, 'person_id': trans.submitter_id,
                'step': 6, 'message': 'verified', 'status': 'success'
            }
            transaction['metadata'] = metadata
            transaction['kv_pairs'] = kv_list
            transaction_results['transactions'][trans.id] = transaction
            transaction_results['times'][entry.get('updated')] = trans.id

        return transaction_results

    @staticmethod
    def _get_file_key_values(file_entries):
        if not file_entries:
            return file_entries
        file_keys = FileKeyValue.select(
            Keys.key, Values.value, FileKeyValue.file
        ).join(Keys, on=(Keys.id == FileKeyValue.key)) \
         .join(Values, on=(Values.id == FileKeyValue.value)) \
         .where(FileKeyValue.file << file_entries.keys()).dicts()

        fkv_list = {}
        for fkv in file_keys:
            file_id = fkv.pop('file')
            if file_id not in fkv_list.keys():
                fkv_list[file_id] = [fkv]
            else:
                fkv_list[file_id].append(fkv)

        enhanced_file_entries = {}
        for (file_id, file_entry) in file_entries.items():
            if file_id in fkv_list.keys():
                file_entry['key_values'] = fkv_list[file_id]
            else:
                file_entry['key_values'] = {}
            enhanced_file_entries[file_id] = file_entry

        return enhanced_file_entries

    @staticmethod
    def _get_base_transaction_metadata(transaction_entry, option=None):
        transaction_id = transaction_entry.get('_id')
        files = QueryBase._get_file_list(transaction_id)
        base_metadata = {
            'transaction_id': transaction_id,
            'submitter_id': transaction_entry.get('submitter'),
            'proposal_id': transaction_entry.get('proposal'),
            'instrument_id': transaction_entry.get('instrument'),
            'file_ids': files.keys()
        }
        if option == 'details':
            submitter = Users.get(
                Users.id == transaction_entry.get('submitter')
            ).to_hash()
            proposal = Proposals.get(
                Proposals.id == transaction_entry.get('proposal')
            ).to_hash()
            instrument = Instruments.get(
                Instruments.id == transaction_entry.get('instrument')
            ).to_hash()
            details_metadata = {
                'submitter_name': '{0} {1}'.format(
                    submitter.get('first_name'),
                    submitter.get('last_name')
                ),
                'proposal_name': proposal.get('title'),
                'instrument_name': instrument.get('display_name'),
                'files': QueryBase._get_file_key_values(files)
            }

            base_metadata.update(details_metadata)

        return base_metadata

    @staticmethod
    def compose_help_block_message():
        """Assemble a block of relevant help text to be returned with an invalid request."""
        message = 'You must supply a numeric transaction id '
        message += '(like "/transactioninfo/<transaction_id>")'
        return message
