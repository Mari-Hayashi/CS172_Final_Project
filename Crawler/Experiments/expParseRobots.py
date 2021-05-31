import requests

import os
import sys
import time

from bs4 import BeautifulSoup
from Helpers.PathHandler import PathHandler

DATA_PATH = "data"
line_tuples = []
seed_urls = []
ph = PathHandler()
prefix = "http://"


headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }
)
agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'


if len(sys.argv) == 3 and sys.argv[1] == "--url":
    seed_urls.append(sys.argv[2])
elif len(sys.argv) == 3 and sys.argv[1] == "--file":
    with open(sys.argv[2], "r") as seed_url_file: 
        seed_urls.extend([url.strip() for url in seed_url_file.readlines()])
print(seed_urls) 


for seed in seed_urls:
    robots_url = f"{prefix}{seed}/robots.txt"
    page = requests.get(f"{robots_url}") 
    soup = BeautifulSoup(page.content, "html.parser")
    print(soup.prettify())


    try:
        if f"{seed}" not in ph.get_dir_names(f"{DATA_PATH}/."):
            os.mkdir(f"{DATA_PATH}/{seed}")
        os.mkdir(f"{DATA_PATH}/{seed}/robots")
    except FileExistsError:
        pass
    
    with open(f"{DATA_PATH}/{seed}/robots/robots.txt", "w") as robotsFile:
        robotsFile.write(soup.text) 


"""
    for line in robotsFile:
        data = line.strip().split(maxsplit=1)    
        data[0] = data[0].strip(":")
        if data[0] != "#":
            line_tuples.append(tuple(data))
"""


