#!/bin/python

import EUSTransferSync as transfer_sync

if __name__ == '__main__':
	sync = transfer_sync.EUSTransferSync()
	sync.start_transfer(force=True)
