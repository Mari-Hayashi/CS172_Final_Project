# standard libraries
import ntpath
import os
import glob
import uuid
import base64



# get list of all subfile paths from src_path
def get_file_paths(src_path):
    return [file_path for file_path in glob.glob(src_path + "*.*")]



# returns size of entire path
def get_dir_size(src_path, datatype="b"):
    total_size = 0 
    filepaths = get_file_paths(src_path)
    for filepath in filepaths:
        try:
            total_size += os.path.getsize(filepath)
        except:
            pass   
 
    # transform size to match datatype
    if datatype == "b" or datatype == "byte":
        return total_size
    elif datatype == "k" or datatype == "kb" or datatype == "kilobyte":
        return total_size / 1024
    elif datatype == "m" or datatype == "mb" or datatype == "megabyte":
        return total_size / (1024 ** 2)
    elif datatype == "g" or datatype == "gb" or datatype == "gigabyte":
        return total_size / (1024 ** 3)
    elif datatype == "t" or datatype == "tb" or datatype == "terabyte":
        return total_size / (1024 ** 4)
    else:
        return total_size
   


# returns number of files in path
def get_dir_pages(src_path):
    return len(get_file_paths(src_path)) 




# builds directories up to if not exists, otherwise do nothing
def make_dirs(dest):
    try:
        os.makedirs(dest) 
    except FileExistsError:
        pass 



# unique_filename - DEPRECATED
# filename can get too long
def old_unique_filename(url):
    url_bytes = url.encode("ascii")
    url_encoding = base64.urlsafe_b64encode(url_bytes)
    url_encoding_str = str(url_encoding)[2:-1]



# generates a unique filename
def generate_unique_filename():
    return f"{uuid.uuid4().hex}"



# identify files we do not want to scrape
def non_html_file(url):
    extensions = (".mp3", ".mp4", ".wav", ".ogg", ".jpg", ".png", ".pdf", ".doc")
    if url.endswith(extensions):
        return True
    return False



# extract lines from file
def extract_lines(filenames):
    if type(filenames) == str:
        filenames = [filenames]
    urls = []
    for filename in filenames:
        with open(filename, "r") as file:
            urls.extend([url for url in file.read().split("\n") if url != ""])
    return urls


