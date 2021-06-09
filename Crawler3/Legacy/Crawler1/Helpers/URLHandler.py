import re

URL_PREFIX = "http://"
URL_PREFIX_REGEX = r"(http(s)?:\/\/)?(www\.)?"

# only isolates root link
def root_link(link):
    return no_prefix_link(link).split(sep="/", maxsplit=1)[0]

# removes prefix from link
def no_prefix_link(link):
    return re.sub(URL_PREFIX_REGEX, "", link)

# adds http:// prefix
def add_prefix_link(link):
    return URL_PREFIX + root_link(link)

# gets the robot link
def robots_link(link):
    return URL_PREFIX + root_link(link) + "/robots.txt"

