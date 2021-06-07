import os
import re
import requests
from bs4 import BeautifulSoup
import Helpers.URLHandler as URLHandler
import user_agents

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

def parse_to_dict(text, 

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

class Robot:
    def __init__(self, user_agent):
        self.agents = []
        agents = str(user_agents.parse(user_agent)).split("/")
        for agent in agents:
            self.agents.append((" ".join(re.findall("[a-zA-Z]+", agent)).lower())

    def __parse_line(self, line):
        data = line.strip().split(" ", maxsplit=1)
        data[0] = data[0].strip(":")
        if len(data) != 1 and data[0] != "#":
            return tuple(data[0], data[1])
        return None

    def __is_valid_useragent(self, data):
        if data:
            if data[0] == "User-agent" and data[1] in self.agents:
                return True
        return False

    def __is_valid_link(self, data, link):
        

    def can_visit(self, link):

        # if robots.txt has been saved
        robots_path = DATA_PATH + root + ROBO_PATH + "/robots.txt"
        if os.path.exists(robots_file):   
            with open(robots_path, "r") as robots_file:
                text = robots_file.read()  

        # else, crawl and save
        else:
            robots_link = URLHandler.robots_link(link) 
            page = requests.get(robots_link)
            soup = BeautifulSoup(page.content, "html.parser")
            text = soup.text
            try:
                os.mkdir(DATA_PATH + root + ROBO_PATH)
            except:
                pass
            with open(robots_path, "w") as robots_file:
                robots_file.write(text)

        # parse and read until matching user agent 
        lines = text.split("\n")
        check = False
        for line in lines:
            data = self.__parse_line(line)          
            if self.__is_valid_useragent(data):
                check = True
            else:
                check = False
            if check and self.__is_valid_link(data, link):
                return True  
        return False
