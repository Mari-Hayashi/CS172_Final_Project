import os
from queue import Queue
import sys
import threading
import time


import requests
from bs4 import BeautifulSoup
import Helpers.PathHandler as PathHandler
import Helpers.URLHandler as URLHandler
import Helpers.RoboHandler as RoboHandler

DATA_PATH = "crawl_data/"

class Crawler:
    def __init__(self):
        self.lines = []
        self.seeds = []
        self.threads = []
        self.permissions = dict()
        self.agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        self.headers = requests.utils.default_headers()
        self.headers.update ({'User-Agent':self.agent})
        self.queue = Queue()

    def crawl_worker(self):
        while not self.queue.empty():
            seed = self.queue.get()
            root_link = URLHandler.root_link(seed)
            no_prefix_link = URLHandler.no_prefix_link(seed)
            prefix_link = URLHandler.add_prefix_link(seed)
            robots_link = URLHandler.robots_link(seed)
            print(f"Seed: {seed}")
            print(f"Root Link: {root_link}")
            print(f"No Prefix Link: {no_prefix_link}")
            print(f"Prefix Link: {prefix_link}")
            print(f"Robots Link: {robots_link}")

            seed_dir = DATA_PATH + root_link
            print(f"Seed Directory: {seed_dir}")

            robots = RoboHandler.build_robots(seed)
            page = requests.get(prefix_link)
            soup = BeautifulSoup(page.content, "html.parser")
            # print(f"\n{soup.prettify()}")

    
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
    crawler.multithread_crawl(seeds=urls, threads=5)
