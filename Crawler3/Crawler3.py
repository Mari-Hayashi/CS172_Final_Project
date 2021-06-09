# standard libraries
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

# external libraries
import requests
from bs4 import BeautifulSoup

# custom libraries
import Crawler3.Helpers.FileHandler as FileHandler
import Crawler3.Helpers.URLHandler as URLHandler
from Crawler3.Helpers.TimeHandler import TimeHandler

AGENTS="/Crawler3/agents.txt"
DECODER="filenames.txt"
INPUT="urls.txt"
OUTPUT="htmls"

ATTEMPTS=5
PAGES=100
THREADS=1

CRAWL_INTERVAL=1
LIMIT_INTERVAL=5
TIMEOUT_INTERVAL=3

# Todo-list:
# 1. Add verbose option (time prints & identity) -> DONE
# 2. Incorporate depth into queue tuple -> DONE
# 3. Max_size check and quit crawl_worker if maxed -> DONE
# 4. Randomize header -> DONE
# 5. Add size limit -> DONE
# 6. Robots.txt Functionality -> INCOMPLETE
# 6. Eliminate duplicate files -> INCOMPLETE
# 7. Add documentation (python style) -> INCOMPLETE


class Crawler:
    
    # CLEAN UP
    # MODIFY CONSTRUCTOR ORDER
    def __init__(self, urls=[], output=OUTPUT, decoder=DECODER, size=None, depth=None, pages=None, verbose=False, interval=CRAWL_INTERVAL):

        # misc
        self.threads = []                   # keeps track of running threads
        self.start = time.time()            # keeps track of timer

        # data
        self.agents = AGENTS                # file for rotating agents
        self.visited = set()                # set of links that have already been visited / scraped
        self.visitLock = threading.Lock()   # mutex lock for visited set
        self.decoder = decoder              # file for storing filename conversions
        self.decoderLock = threading.Lock() # mutex lock for filenames.txt
        self.queue = Queue()                # queue for links to crawl
        self.queueLock = threading.Lock()   # mutex lock for accessing queue

        # settings
        self.verbose = verbose              # enable/disable verbose info while crawling
        self.output = output                # output folder for downloads
        self.interval = interval            # how long to wait between scraping next item
        self.maxdepth = depth               # default max depth
        self.maxsize = size                 # default max size in mb to crawl
        self.maxpages = pages               # default max pages

        # internal flags
        self.flagLimit = False              # flag for reaching one of the limits
        self.flagDepth = False              # flag for reaching max depth
        self.flagSize = False               # flag for reaching max download size
        self.flagPages = False              # flag for reaching max pages
        self.flagComplete = False           # flag to signal size worker to end if empty queue

        # set default page limit to 100 if no limit is set
        if not depth and not size and not pages:
            self.pages = PAGES

        # read in list of agents
        with open(os.getcwd() + self.agents, "r") as agents_file:
            self.agents = agents_file.readlines()

        # place full urls into queue
        for url in urls:
            link = URLHandler.add_prefix(url)
            self.queue.put((link, 0))



    # if reached max depth, return true
    def __at_depth_limit(self, curdepth=0):
        if not self.maxdepth:
            return False
        elif curdepth > self.maxdepth:
            self.flagDepth = True
        return self.flagDepth



    # if reached max size, return true
    def __at_size_limit(self):
        return self.flagSize



    # if reached max pagecount, return true
    def __at_page_limit(self):
        return self.flagPages
 

    
    # if reached any limit, return true
    def __at_limit(self):
        return self.flagLimit
        


    # returns a random header
    def __random_header(self):
        random_index = random.randint(0, len(self.agents) - 1)
        random_agent = self.agents[random_index]
        headers = requests.utils.default_headers()
        headers.update({"User-Agent": random_agent})


    
    # download html to file and update 
    def __download_html(self, url, text):
        url_encoding_str = FileHandler.generate_unique_filename()

        try:
            self.decoderLock.acquire()
            with open(self.decoder, "a+") as names_file:
                names_file.write(f"{url_encoding_str}.html {url}\n")
        finally:
            self.decoderLock.release()

        # save html document into crawl_data/ directory
        html_name = f"{self.output}/{url_encoding_str}.html"
        FileHandler.make_dirs(f"{self.output}")
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
            page = requests.get(url, timeout=TIMEOUT_INTERVAL, headers=self.__random_header())
        except requests.exceptions.RequestException as e:
            if self.verbose:
                print(f"Crawler.__scrape_text: Could not retrieve {url[:20]} due to {e}")
            return None, None
        except Exception as e:
            if self.verbose:
                print(f"Crawler.__scrape_text: Could not retrieve {url[:20]} due to Unknown {e}")
            return None, None

        # identify all neighbor links
        neighbors = []
        soup = BeautifulSoup(page.content, "html.parser")
        for elem in soup.find_all("a"):
            if "href" in elem.attrs:
                link = elem.attrs["href"]
                clean_link = URLHandler.create_link_from_seed(url, link)
                if clean_link:
                    neighbors.append(clean_link) 

        return page.text, neighbors




    # crawl url, download and grab links
    def __crawl(self, url, cur_depth):

        # exit if visited, otherwise add to visited set
        if not self.__add_to_visited(url):
            return "visited"

        # scrape text, exit if error scraping
        text, neighbors = self.__scrape_text(url)
        if not text:
            return "html error"

        # exit if duplicate page (in works)
        if self.__is_duplicate(url):
            return "duplicate"

        # download text to file
        self.__download_html(url, text)

        # append neighbors to queue
        self.__add_neighbors(neighbors, cur_depth)

        return "success"



    # thread checks to see if limit has been surpassed
    def __limit_worker(self, src_path, interval=LIMIT_INTERVAL):

        timer = TimeHandler(name="Limit Checker", verbose=self.verbose)
        timer.start(desc=f"START LIMIT CHECKING at {src_path}")
        cur_size = 0
        cur_pages = 0

        # update condition for page and depth checking
        while True:

            # update size and pages
            time.sleep(interval) 
            cur_size = FileHandler.get_dir_size(src_path, datatype="mb")
            cur_pages = FileHandler.get_dir_pages(src_path)

            # check size limit
            if self.maxsize:
                timer.end(desc=f"CRAWLED {cur_size:.2f} / {self.maxsize:.2f} MB") 
                if cur_size >= self.maxsize:
                    self.flagSize = True
                    timer.signal(desc=f"has reached size limit, shutting off")  
                    break
            else: 
                timer.end(desc=f"CRAWLED {cur_size:.2f} MB") 


            # check page limit
            if self.maxpages:
                timer.end(desc=f"CRAWLED {cur_pages} / {self.maxpages} pages") 
                if cur_pages >= self.maxpages:
                    self.flagPages = True
                    timer.signal(desc=f"has reached page limit, shutting off")  
                    break
            else:
                timer.end(desc=f"CRAWLED {cur_pages} pages") 


            # check depth limit
            if self.maxdepth:
                if self.__at_depth_limit():
                    self.flagDepth = True
                    timer.signal(desc=f"has reached depth limit, shutting off")
                    break


            # check threads have finished
            if self.flagComplete:
                timer.signal(desc=f"queue is empty, shutting off")
                break

        # update flag limit to end threads
        self.flagLimit = True



    # crawl worker for multithreading
    def __crawl_worker(self, identity):

        timer = TimeHandler(name=f"Crawler #{identity}", verbose=self.verbose)
        tries = 0

        while tries < ATTEMPTS:
            tries += 1
            while not self.queue.empty() and not self.__at_limit():

                # extract link from queue
                time.sleep(self.interval) 
                item = self.queue.get()                         
                url = item[0]
                cur_depth = item[1]

                # skip link if beyond depth
                if self.__at_depth_limit(cur_depth):
                    if self.verbose:
                        print(f"Crawler #{identity} exceeded max depth limit {self.maxdepth + 1}")
                    continue

                # skip link if beyond size
                if self.__at_size_limit():
                    if self.verbose:
                        print(f"Crawler #{identity} reached max size limit {self.maxsize:.2f} mb")
                    continue
        
                # skip link if beyond page limit
                if self.__at_page_limit():
                    if self.verbose:
                        print(f"Crawler #{identity} reached max page limit {self.maxpages} pages")
                    continue

                # skip link if non-html file
                if FileHandler.non_html_file(url):
                    if self.verbose:
                        print(f"Crawler #{identity}   {URLHandler.no_prefix(url)[:15]} is not a standard html")
                    continue

                # otherwise crawl the link
                timer.start(desc=f"START CRAWL {URLHandler.no_prefix(url)[:15]}... DEPTH: {cur_depth}")
                status = self.__crawl(url, cur_depth)
                self.queue.task_done()
                timer.end(desc=f"END CRAWL {URLHandler.no_prefix(url)[:15]}... DEPTH: {cur_depth}")
                tries = 0

            if tries == 0:
                timer.start(desc=f"idling")
            time.sleep(3)
        timer.start(desc=f"shutting off")



    # add neighbors
    def __add_neighbors(self, neighbors, cur_depth):
        try:
            self.queueLock.acquire()
            for neighbor in neighbors:
                self.queue.put((neighbor, cur_depth + 1))
        finally:
            self.queueLock.release()



    # add urls
    def add_urls(self, url=None, urls=[]):
        if url:    
            urls.append(url)
        for item in urls:
            link = URLHandler.add_prefix(item)
            self.queue.put((link, 0)) 



    # crawling
    def crawl(self, threads=THREADS):
        
        # one thread to check the size if flagged
        limit_thread = threading.Thread(target=self.__limit_worker, args=(f"{self.output}/",))
        limit_thread.start()

        # create and start threads for crawling
        for i in range(threads):
            t = threading.Thread(target=self.__crawl_worker, args=(i,))
            self.threads.append(t)
            t.start()

        # wait for threads to finish before resuming multithreading
        for i in range(threads):
            self.threads[i].join() 

        # output results and signal limit thread to terminate
        self.flagComplete = True
        total_size = FileHandler.get_dir_size(f"{self.output}/", datatype="mb")
        total_pages = FileHandler.get_dir_pages(f"{self.output}/")
        print(f"Crawling finished with a total of {total_size:.2f} mb and {total_pages} pages")
        time.sleep(3)
 
        # zip the file, remove temp directory
        shutil.make_archive(self.output, 'zip', self.output)
        shutil.rmtree(self.output, ignore_errors=True)


        

# run parser and crawler
def run():

    # custom help text
    examples_prompt=f"""Examples:
    
    python {sys.argv[0]} google.com                             ===>   Crawl google.com with default depth 1
    python {sys.argv[0]} google.com bing.com yahoo.com          ===>   Crawl multiple links
    python {sys.argv[0]} google.com --verbose                   ===>   Crawl google.com with verbose prints
    python {sys.argv[0]} --urlfiles urls.txt                    ===>   Crawl urls listed in urls.txt file
    python {sys.argv[0]} --urlfiles urls.txt -threads 5         ===>   Crawl urls.txt with 5 threads"""


    # name arguments
    parser = argparse.ArgumentParser(description="Crawl websites and store html files locally", epilog=examples_prompt, formatter_class=argparse.RawDescriptionHelpFormatter)
    nameGroup = parser.add_argument_group("NAMES", "Set input and output names")
    nameGroup.add_argument("url", help="urls to scrape, use the --urlfile flag to load urls from a file instead", nargs="*")
    nameGroup.add_argument("--urlfile", help="input file with urls", default=INPUT)
    nameGroup.add_argument("--output", help="output zipfile, default = htmls/", default=OUTPUT)
    nameGroup.add_argument("--decoder", help="decoder of file names,  default = filenames.txt", default=DECODER)

    # limit arguments
    limitGroup = parser.add_argument_group("LIMITS", "Set limits on crawling, default = 100 pages")
    limitGroup.add_argument("-depth", help="depth of crawling", type=int)
    limitGroup.add_argument("-size", help="crawling size", type=int)
    limitGroup.add_argument("-pages", help="number of pages", type=int)

    # setting arguments
    settingGroup = parser.add_argument_group("SETTINGS", "Set settings for crawler")
    settingGroup.add_argument("-threads", help="set number of threads, default = 1", type=int, nargs="?", default=THREADS, const=THREADS)
    settingGroup.add_argument("-interval", help="set crawling wait interval, default = 1", nargs="?", default=CRAWL_INTERVAL, const=CRAWL_INTERVAL, type=int)
    settingGroup.add_argument("-verbose", help="enable verbose actions, default = false", action="store_true")
    settingGroup.add_argument("-clean", help="clean old crawled data, default = false", action="store_true")
    

    # extract urls from filename
    args = parser.parse_args()
    if args.urlfile:
        urls = FileHandler.extract_lines(args.urlfile)
    else:
        urls = [url for url in args.url]  


    # clean files
    if args.clean:
        shutil.rmtree(args.output, ignore_errors=True)
        try:
            os.remove(args.decoder)
        except:
            pass
        

    # instantiate and run crawler        
    crawler = Crawler(urls=urls, depth=args.depth, size=args.size, pages=args.pages, verbose=args.verbose, interval=args.interval)
    crawler.crawl(threads=args.threads)




if __name__ == "__main__":
    run()



