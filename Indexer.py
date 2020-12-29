from indexhandler import *
import sys
from general import *

if __name__ == '__main__':
    PROJECT_NAME = 'Indexer'
    create_project_dir(PROJECT_NAME)
    create_index_files(PROJECT_NAME)
    TEMP_INDEX_FILE = PROJECT_NAME + 'tempIndex.pkl'
    GENERAL_INDEX_FILE = PROJECT_NAME + 'generalIndex.pkl'
    MAX_NUMBER_OF_INDEXES = sys.argv[1]
    keep_old_files = sys.argv[2]
    tempUpdate = sys.argv[3]
    generalUpdate = sys.argv[4]
    if keep_old_files is False:
        delete_data_files(PROJECT_NAME)
    initIndexProcess(tempUpdate, generalUpdate, MAX_NUMBER_OF_INDEXES)
