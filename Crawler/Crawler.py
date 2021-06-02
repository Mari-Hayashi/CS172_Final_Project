import os
from queue import Queue
import re
import sys
import threading
import time


import requests
import urllib.robotparser
from bs4 import BeautifulSoup
import Helpers.PathHandler as PathHandler
import Helpers.URLHandler as URLHandler

DATA_PATH = "crawl_data/"

class Crawler:
    def __init__(self):
        self.visited = set()
        self.threads = []
        self.agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        self.headers = requests.utils.default_headers()
        self.headers.update ({'User-Agent':self.agent})
        self.queue = Queue()
        self.setlock = threading.Lock()
        self.start = time.time()

    def crawl(self, link, root):
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser") 
        for link in soup.find_all("a"):
            if "href" in link.attrs:
                new_link = link.attrs["href"] 
                if new_link[0] == "#":
                    continue
                elif new_link[0] == "/":
                    self.queue.put(root + new_link)
                else:
                    new_link = URLHandler.no_prefix_link(new_link) 
                    self.queue.put(new_link)
        return str(soup)

    def crawl_worker(self):
        while not self.queue.empty():
            start = time.time()
            seed = self.queue.get()
            root_link = URLHandler.root_link(seed)
            no_prefix_link = URLHandler.no_prefix_link(seed)
            prefix_link = URLHandler.add_prefix_link(seed)
            robots_link = URLHandler.robots_link(seed)
            seed_dir = DATA_PATH + root_link
            print(f"{seed} started at {start - self.start:.2f}")

            update = False
            try:
                self.setlock.acquire()
                if prefix_link not in self.visited:
                    update = True 
                    self.visited.add(prefix_link)
                    print(f"{seed} has not been visited!") 
                else:
                    print(f"{seed} already visited!") 

            # check if visited
            # check robots.txt
            # check duplicates

            finally:
                self.setlock.release()    
                time.sleep(1)
                
            if update:
                html = self.crawl(prefix_link)
                file_link = re.sub("/", ".", no_prefix_link)
                with open(DATA_PATH + f"{root_link}/{file_link}", 'w') as html_file:
                    html_file.write(html)
                print(f"{seed} is saved to disk")

                # save results
                # add other neighbors to queue
            print(f"{seed} took {time.time() - start:.2f} seconds")
            print()
    
    def multithread_crawl(self, seeds, threads=5):

        # place seeds into queue
        for seed in seeds: 
            self.queue.put(URLHandler.no_prefix_link(seed))

        # run workers that will pull from queue
        for i in range(threads):
            t = threading.Thread(target=self.crawl_worker, args=())
            self.threads.append(t)
            t.start()

        # wait for all threads to finish before continuing
        for i in range(threads):
            self.threads[i].join()


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--file":
        with open("urls.txt", "r") as url_file:
            urls = [url.strip("\n") for url in url_file.readlines()]
    elif len(sys.argv) == 3 and sys.argv[1] == "--url":
        urls = [sys.argv[2]]
    else:
        print("python Crawler.py --url google.com") 
        print("python Crawler.py --file urls.txt")
        sys.exit(1)

    crawler = Crawler()
    crawler.multithread_crawl(seeds=urls, threads=12)
