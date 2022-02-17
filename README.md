# SearchEngine-IRProject2020
An information retrieval project that It Is made it with pair
programming, 
the project includes:
website crawling, text extraction from html, creation of un inverted index , calculate
cosine similarity with TF-IDF metrics and query processing capabilities. All the parts of
the engine support multithreading.

## Installation

This repository is tested on Python 3.6.
With pip: install the "requirements.txt"
Run the Python interpreter and type the commands:
```
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('stopwords')
```
## How to use it:

### Crawler:
It is responsible for Crawling pages, extracting text from HTML and storing files such as: pages that have been visited (crawled.txt), 
the pages that are in order to visit (queue.txt) and two dictionaries that hold the title and text of every page.

Run the Crawler script from terminal:
terminal must be like: crawler.py https://www.geeksforgeeks.org/  100 1 4 

Parameters in order: the link of first page that crawler will start-> string, the number of crawls that user wants->int,
     keep or not old files-> flag(0,1), number of threads to use -> int. 

### Indexer:
implements the creation of the inverted list and all
additional directories for queryprocessor implementation. In order to index,  the crawler files must exist.

Terminal must be like: Indexer.py n flag threads. N-> Number of pages, flag-> (0,1) keep or not old files, threads-> int the number of threads 

### Query Processor:
Run the main.py to make queries, interact with the interface and customize the results by choosing the ones you prefer.
