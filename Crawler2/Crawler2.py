import argparse
import base64
import os
from queue import Queue
import random
import re
import sys
import threading
import time

import requests
from bs4 import BeautifulSoup
import Helpers.PathHandler as PathHandler
import Helpers.URLHandler as URLHandler

CRAWL_DATA="crawl_data"
FILENAME="filenames.txt"
AGENTS="agents.txt"

# Todo-list:
# 1. Add verbose option (time prints & 
# 2. Incorporate depth into queue tuple
# 3. Max_size check and quit crawl_worker if maxed
# 4. Add documentation (python style)


        class Crawler:
        def __init__(self, urls=[], size=None, depth=None, attempts=10, verbose=False, filename=FILENAME):
        self.visited = set()                # set of links that have already been visited / scraped
        self.visitLock = threading.Lock()   # mutex lock for visited set
        self.filename = filename            # file for storing filename conversions
        self.fileLock = threading.Lock()    # mutext lock for filenames.txt

        self.threads = []                   # keeps track of running threads
        self.start = time.time()            # keeps track of timer
        self.queue = Queue()                # queue for links to crawl

        self.maxdepth = depth               # default max depth
        self.size = 0                       # crawled size in mb
        self.maxsize = size                 # default max size in mb to crawl
        self.attempts = attempts            # number of attempts from each thread to access queue before closing
self.verbose = verbose              # enable/disable verbose info while crawling

# set default depth to 5 if no limit is set
if not depth and not size:
self.maxdepth = 5

# read in list of agents
with open(AGENTS, "r") as agents_file:
self.agents = agents_file.readlines()

# place full urls into queue
    for url in urls:
    link = URLHandler.add_prefix(url)
self.queue.put(link)



# returns a random header
    def __random_header(self):
        random_index = random.randint(0, len(self.agents) - 1)
    random_agent = self.agents[random_index]
        headers = requests.utils.default_headers()
        headers.update({"User-Agent": random_agent})



# download html to file and update 
        def __download_html(self, url, text):

# write encoded filename down
            print(url)
    url_bytes = url.encode("ascii")
    url_encoding = base64.urlsafe_b64encode(url_bytes)
url_encoding_str = str(url_encoding)
    try:
self.fileLock.acquire()
    with open(FILENAME, "a+") as names_file:
    names_file.write(f"{url_encoding_str} {url}\n")
    finally:
self.fileLock.release()

# save html document into crawl_data/ directory
    html_name = f"{CRAWL_DATA}/{url_encoding_str}"
    PathHandler.make_dirs(f"{CRAWL_DATA}")
    with open(html_name, "w") as html_file:
html_file.write(text)



# come back to do duplicate page check
    def __is_duplicate(self, url):
        return False



# check if url is visited, if not, acquire lock and visit
        def __add_to_visited(self, url):
            result = True
            try:
            self.visitLock.acquire()
            if url in self.visited:
            result = False 
            else:
            self.visited.add(url)
            finally:
                self.visitLock.release()
                return result



# scrape page for text
                def __scrape_text(self, url):

# make page request
                    try:
page = requests.get(url)
    except URLError as ue:
    print(f"Crawler.__scrape_text: Could not retrieve {url} due to {ue}")
    return None
    except:
    print(f"Crawler.__scrape_text: Could not retrieve {url} due to Unknown Error")

# identify all neighbor links to crawl
    neighbors = []
    soup = BeautifulSoup(page.content, "html.parser")
    for elem in soup.find_all("a"):
    if "href" in elem.attrs:
    link = elem.attrs["href"]
clean_link = URLHandler.create_link_from_seed(url, link)
    if clean_link:
neighbors.append(clean_link) 

    return soup.text, neighbors



# add urls
    def add_urls(self, url=None, urls=[]):
        if url:    
        urls.append(url)
        for item in urls:
    link = URLHandler.add_prefix(item)
    self.queue.put(link) 



# crawl url, download and grab links
    def crawl(self, url):

# exit if visited, otherwise add to visited set
        if not self.__add_to_visited(url):
            return None

            print("visited")

# exit if duplicate
            if self.__is_duplicate(url):
                return None

                print("duplicate")

# scrape text, exit if error scraping
text, neighbors = self.__scrape_text(url)
    if not text:
    return None

    print(f"text and neighbors {text[0:10]}")

# download text to file
self.__download_html(url, text)

    print("downloaded file")

# append neighbors to queue
    for neighbor in neighbors:
self.queue.put(neighbor)

    print(f"added neighbors {neighbors}")

# crawl worker for multithreading
    def crawl_worker(self, identity):

# make 10 attempts to check queue for links before closing thread
        tries = self.attempts
        while tries < 10:
        tries += 1
        if not self.queue.empty():
            while not self.queue.empty():
                url = self.queue.get()
                print(f"{identity} has obtained {url}")
    self.crawl(url)
    self.queue.task_done()
time.sleep(1)
    tries = 0
time.sleep(3)



# multithread crawling
    def multithread_crawl(self, threads=12):

# create and start threads for crawling
        for i in range(threads):
    t = threading.Thread(target=self.crawl_worker, args=(i,))
    self.threads.append(t)
    t.start()

# wait for threads to finish before resuming multithreading
    for i in range(threads):
        self.threads[i].join() 



        def run():
            parser = argparse.ArgumentParser(description="Crawl websites and store html files locally")
            parser.add_argument("inputs", help="<Required> urls to scrape, use the --filename flag to load urls from a file instead", nargs="+")
            parser.add_argument("--filename", help="name of file with urls in this format:\n\t<url1>\n\t<url2>\n\t<url3>", action="store_true")     
            parser.add_argument("--threads", help="number of threads", type=int)
    parser.add_argument("--verbose", help="turn on verbose prints", action="store_true")
            group1 = parser.add_mutually_exclusive_group()
            group1.add_argument("--depth", help="depth of crawling", type=int)
    group1.add_argument("--size", help="crawling size", type=int)
            args = parser.parse_args()

            if args.filename:
            urls = []
            for filename in args.inputs:
            with open(filename, "r") as url_file:
    file_urls = [url for url in url_file.read().split("\n") if url != ""]  
urls.extend(file_urls)
    else:
    urls = [url for url in args.inputs]  

    crawler = Crawler(urls=urls, depth=args.depth, size=args.size)
crawler.multithread_crawl(threads=12)


    if __name__ == "__main__":
run()


