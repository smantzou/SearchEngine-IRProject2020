from indexhandler import *
import sys
from general import *
from timeit import default_timer as timer

if __name__ == '__main__':
    PROJECT_NAME = 'Indexer'
    create_project_dir(PROJECT_NAME)
    create_index_files(PROJECT_NAME)
    TEMP_INDEX_FILE = PROJECT_NAME + 'invertedIndex.pkl'
    MAX_NUMBER_OF_INDEXES = sys.argv[1]
    keep_old_files = sys.argv[2]
    if keep_old_files is False:
        delete_data_files(PROJECT_NAME)
    start = timer()
    initIndexProcess(MAX_NUMBER_OF_INDEXES)
    end = timer()
    print('Elapsed time : ' + str(end-start))
