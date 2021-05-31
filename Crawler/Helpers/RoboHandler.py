import re
import requests
from bs4 import BeautifulSoup
import Helpers.URLHandler as URLHandler

DATA_PATH = "crawl_data/"
ROBO_PATH = "/robots"

def print_tuples(tuples):
    for item in tuples:
        print(item)

def parse_to_tuples(root, text):
    tuples = []
    text = text.split("\n")
    for line in text:
        data = line.strip().split(" ", maxsplit=1) 
        data[0] = data[0].strip(":")
        if len(data) != 1 and data[0] != "#":
            tuples.append((root, data[0], data[1]))
    return tuples 

def build_robots(link):
    root = URLHandler.root_link(link)
    robots_path = DATA_PATH + root + ROBO_PATH

    # if dir does not exist
    robots_link = URLHandler.robots_link(link)
    user_agent = "*"    
    page = requests.get(robots_link)
    soup = BeautifulSoup(page.content, "html.parser")
    text = soup.text 
    tuples = parse_to_tuples(root, text)
    print_tuples(tuples)
    return {}
