import requests
import urllib3
import sys
from bs4 import BeautifulSoup

if len(sys.argv) == 2:
    url = sys.argv[1]
    print(sys.argv[1], " ", len(sys.argv))
else:
    url = "https://google.com/robots.txt"

# default headers that requests uses
headers = requests.utils.default_headers()

# make custom updates to headers
headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }
)

agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())
