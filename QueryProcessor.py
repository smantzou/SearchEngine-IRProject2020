import sys
from queryHandler import processQuery


if __name__ == '__main__':
    query = sys.argv[1:]
    topKUrls = processQuery()

