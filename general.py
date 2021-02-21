import os
import pickle
import shutil
from tld import get_tld


def create_project_dir(directory):
    """Creation of directory"""
    if not os.path.exists(directory):
        print("Creating project " + directory)
        os.makedirs(directory)


def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


def create_index_files(project):
    """Creation of files in Indexer directory for indexing"""
    tempIndex = project + '/invertedIndex.pkl'
    position = project + '/position_dict.pkl'
    if not os.path.isfile(tempIndex):
        write_file(tempIndex, '')
    if not os.path.isfile(position):
        write_file(position, '')


def create_data_files(project_name, base_url):
    """creation of crawler files in crawler directory"""
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    dictionary = project_name + '/dictionary.pkl'
    titles = project_name + '/titles.pkl'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')
    if not os.path.isfile(dictionary):
        write_file(dictionary, '')
    if not os.path.isfile(titles):
        write_file(titles, '')


def delete_data_files(project_name):
    """Delete all previous entries in the folder"""
    if os.path.isdir(project_name):
        shutil.rmtree(project_name)


def append_to_file(path, data):
    """Add data onto an existing file"""
    with open(path, 'a', encoding="utf-8", errors="ignore") as file:
        file.write(data)
        file.write("\n")


def delete_file_contents(path):
    """Delete the contents of a file"""
    with open(path, 'w'):
        pass


def file_to_set(file_name) -> set:
    """Read a file and convert each line to set item"""
    results = set()
    with open(file_name, 'rt', encoding="UTF-8", errors="ignore") as f:
        for line in f:
            results.add(line.replace('\n', ''))
        return results


def set_to_file(links, file):
    """Iterate through a set , each item will be a new line in the file"""
    delete_file_contents(file)
    for link in sorted(links):
        res = get_tld(link, as_object=True, fail_silently=True)
        if res is not None:
            if res.fld is not None:
                append_to_file(file, link)


def dict_to_file(textDict, file):
    """Dumps the dictionary of text into file (using pickle)"""
    with open(file, 'wb') as file:
        pickle.dump(textDict, file)
        file.close()


def file_to_dict(file):
    """From file to dict"""
    if os.path.getsize(file) > 0:
        with open(file, 'rb') as file:
            new_dict = pickle.load(file)
            file.close()
            return new_dict
    else:
        return dict()


def isEnglish(s):
    """check if text in page is English"""
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
