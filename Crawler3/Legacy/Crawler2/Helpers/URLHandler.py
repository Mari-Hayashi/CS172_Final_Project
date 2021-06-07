import re

URL_PREFIX = "http://"
URL_PREFIX_REGEX = r"(http(s)?:\/\/)?(www\.)?"

# only isolates root link
def root(link):
    return no_prefix(link).split(sep="/", maxsplit=1)[0]

# removes prefix from link
def no_prefix(link):
    return re.sub(URL_PREFIX_REGEX, "", link)

# adds http:// prefix
def add_prefix(link):
    return URL_PREFIX + no_prefix(link)

# gets the robot link
def robots(link):
    return URL_PREFIX + root(link) + "/robots.txt"

# create a full link in case it is a relative link
def create_link_from_seed(seed, new_link):

    # if empty link, pass 
    if len(new_link) == 0:
        return None

    # if comment, pass
    elif new_link[0] == "#":
        return None

    # if relative link
    elif new_link[0] == "/":
        return add_prefix(seed) + new_link
    
    # if full link, just return with consistent prefix     
    return add_prefix(new_link)
