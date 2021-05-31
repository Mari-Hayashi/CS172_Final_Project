from urllib.robotparser import RobotFileParser
import sys

if len(sys.argv) >= 2:
    url = sys.argv[1]
else:
    url = "https://google.com/robots.txt"


agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
robot_parser = RobotFileParser(url)
robot_parser.read()
