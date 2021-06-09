import argparse
import base64
import os
from queue import Queue
import random
import re
import shutil
import sys
import threading
import time

import requests
from bs4 import BeautifulSoup
import Crawler3.Helpers.PathHandler as PathHandler
import Crawler3.Helpers.URLHandler as URLHandler
import Crawler3.Helpers.TimeHandler as TimeHandler

CRAWL_DATA="htmls"
FILENAME="filenames.txt"
AGENTS="Crawler3/agents.txt"
DEFAULT_OUTPUT="htmls"

# Todo-list:
# 1. Add verbose option (time prints & identity) -> DONE
# 2. Incorporate depth into queue tuple -> DONE
# 3. Max_size check and quit crawl_worker if maxed -> DONE
# 4. Randomize header -> DONE
# 5. Eliminate duplicate files ->
# 6. 
# 7. Add documentation (python style)


class Crawler:
    def __init__(self, urls=[], size=None, depth=None, attempts=5, verbose=False, filename=FILENAME, interval=1, output=CRAWL_DATA):
        self.visited = set()                # set of links that have already been visited / scraped
        self.visitLock = threading.Lock()   # mutex lock for visited set
        self.filename = filename            # file for storing filename conversions
        self.fileLock = threading.Lock()    # mutex lock for filenames.txt
        self.queue = Queue()                # queue for links to crawl
        self.queueLock = threading.Lock()   # mutex lock for accessing queue

        self.threads = []                   # keeps track of running threads
        self.start = time.time()            # keeps track of timer


        self.ismaxdepth = False             # flag for reaching max depth
        self.maxdepth = depth               # default max depth
        self.maxsize = size                 # default max size in mb to crawl
        self.full = False                   # boolean flag to signify crawled max data
        self.attempts = attempts            # number of attempts from each thread to access queue before closing
        self.verbose = verbose              # enable/disable verbose info while crawling
        self.interval = interval            # how long to wait between scraping next item
        self.output = output                # output folder for downloads

        # set default depth to 1 if no limit is set
        if not depth and not size:
            self.maxdepth = 1

        # read in list of agents
        with open(AGENTS, "r") as agents_file:
            self.agents = agents_file.readlines()

        # place full urls into queue
        for url in urls:
            link = URLHandler.add_prefix(url)
            self.queue.put((link, 0))



    # returns a random header
    def __random_header(self):
        random_index = random.randint(0, len(self.agents) - 1)
        random_agent = self.agents[random_index]
        headers = requests.utils.default_headers()
        headers.update({"User-Agent": random_agent})



    # download html to file and update 
    def __download_html(self, url, text):
        url_encoding_str = PathHandler.generate_unique_filename()

        try:
            self.fileLock.acquire()
            with open(FILENAME, "a+") as names_file:
                names_file.write(f"{url_encoding_str}.html {url}\n")
        finally:
            self.fileLock.release()

        # save html document into crawl_data/ directory
        html_name = f"{self.output}/{url_encoding_str}.html"
        PathHandler.make_dirs(f"{self.output}")
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
    def __scrape_text(self, url, timeout=1):

        # make page request
        try:
            page = requests.get(url, timeout=timeout, headers=self.__random_header())
            # page = requests.get(url, timeout=timeout)
        except requests.exceptions.RequestException as e:
            print(f"Crawler.__scrape_text: Could not retrieve {url} due to {e}")
            return None, None
        except Exception as e:
            print(f"Crawler.__scrape_text: Could not retrieve {url} due to Unknown {e}")
            return None, None

        # identify all neighbor links to crawl
        neighbors = []
        soup = BeautifulSoup(page.content, "html.parser")
        for elem in soup.find_all("a"):
            if "href" in elem.attrs:
                link = elem.attrs["href"]
                clean_link = URLHandler.create_link_from_seed(url, link)
                if clean_link:
                    neighbors.append(clean_link) 

        return page.text, neighbors



    # add urls
    def add_urls(self, url=None, urls=[]):
        if url:    
            urls.append(url)
        for item in urls:
            link = URLHandler.add_prefix(item)
            self.queue.put((link, 0)) 

    
    # thread that checks the size
    def size_worker(self, src_path, interval=10):

        timer = TimeHandler.TimeHandler(name="Size Checker", verbose=self.verbose)
        timer.start(desc=f"START SIZE CHECKING at {src_path}")
        cur_size = 0
        while cur_size <= self.maxsize:
            time.sleep(interval)
            cur_size = PathHandler.get_dir_size(src_path, datatype="mb")
            timer.end(desc=f"CRAWLED {cur_size:.3f} out of {self.maxsize:.3f} MB") 
            if len(self.threads) == 0:
                return 
        timer.start(desc=f"SIZE has hit capacity, shutting off")  
        self.full = True



    # crawl url, download and grab links
    def crawl(self, url, cur_depth):

        # exit if visited, otherwise add to visited set
        if not self.__add_to_visited(url):
            return None

        # exit if duplicate
        if self.__is_duplicate(url):
            return None

        # scrape text, exit if error scraping
        text, neighbors = self.__scrape_text(url)
        if not text:
            return None

        # download text to file
        self.__download_html(url, text)


        # append neighbors to queue
        for neighbor in neighbors:
            try:
                self.queueLock.acquire()
                self.queue.put((neighbor, cur_depth + 1))
            finally:
                self.queueLock.release()

    # crawl worker for multithreading
    def crawl_worker(self, identity):

        timer = TimeHandler.TimeHandler(name=f"Crawler #{identity}", verbose=self.verbose)

        # make 10 attempts to check queue for links before closing thread
        tries = 0
        while tries < self.attempts:
            tries += 1
            if not self.queue.empty() and not self.full and not self.ismaxdepth:
                while not self.queue.empty() and not self.full and not self.ismaxdepth:
        
                    # attempt to get from queue
                    try:
                        item = self.queue.get() 
                    except Queue.Empty:
                        print(f"Crawler #{identity} Queue is empty!")
                        continue
                        
                    url = item[0]
                    cur_depth = item[1]

                    # skip link if beyond depth
                    if self.maxdepth:
                        if cur_depth > self.maxdepth:
                            print("Crawler #{identity} hit max depth")
                            self.ismaxdepth = True
                            continue

                    # skip link if non-html file
                    if PathHandler.non_html_file(url):
                        continue

                    timer.start(desc=f"START CRAWL {URLHandler.root(url)} DEPTH: {cur_depth}")
                    status = self.crawl(url, cur_depth)
                    self.queue.task_done()
                    timer.end(desc=f"END CRAWL {URLHandler.root(url)} DEPTH: {cur_depth}")
                    time.sleep(self.interval)

                timer.start(desc=f"idling")
                tries = 0
            time.sleep(3)
        timer.start(desc=f"shutting off")



    # multithread crawling
    def multithread_crawl(self, threads=12):
        
        # one thread to check the size if flagged
        if self.maxsize:
            size_thread = threading.Thread(target=self.size_worker, args=(f"{self.output}/",))
            size_thread.start()

        # create and start threads for crawling
        for i in range(threads):
            t = threading.Thread(target=self.crawl_worker, args=(i,))
            self.threads.append(t)
            t.start()

        # wait for threads to finish before resuming multithreading
        for i in range(threads):
            self.threads[i].join() 
 
        # zip the file
        shutil.make_archive(self.output, 'zip', self.output)


# run parser and crawler
def run():

    # custom help text
    examples_prompt=f"""Examples:
    
    python {sys.argv[0]} google.com                             ===>   Crawl google.com with default depth 1
    python {sys.argv[0]} google.com bing.com yahoo.com          ===>   Crawl multiple links
    python {sys.argv[0]} google.com --verbose                   ===>   Crawl google.com with verbose prints
    python {sys.argv[0]} --filename urls.txt                    ===>   Crawl urls listed in urls.txt file
    python {sys.argv[0]} --filename urls.txt --threads 5        ===>   Crawl urls.txt with 5 threads"""

    # generate argument parser
    parser = argparse.ArgumentParser(description="Crawl websites and store html files locally", epilog=examples_prompt, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("inputs", help="<Required> urls to scrape, use the --filename flag to load urls from a file instead", nargs="+")
    parser.add_argument("--filename", help="name of file with urls", action="store_true")     
    parser.add_argument("--threads", help="number of threads", type=int, nargs="?", default=1, const=1)
    parser.add_argument("--verbose", help="turn on verbose option", action="store_true")
    parser.add_argument("--interval", help="set wait interval, default = 1", nargs="?", default=1, const=1, type=int)
    
    # remove mutually exclusive in the future
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument("--depth", help="depth of crawling", type=int)
    group1.add_argument("--size", help="crawling size", type=int)
    args = parser.parse_args()

    # extract urls from filename
    if args.filename:
        urls = []
        for filename in args.inputs:
            with open(filename, "r") as url_file:
                file_urls = [url for url in url_file.read().split("\n") if url != ""]  
            urls.extend(file_urls)
    else:
        urls = [url for url in args.inputs]  
        
    crawler = Crawler(urls=urls, depth=args.depth, size=args.size, verbose=args.verbose, interval=args.interval)
    crawler.multithread_crawl(threads=args.threads)



if __name__ == "__main__":
    run()
