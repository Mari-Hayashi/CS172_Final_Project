# standard libraries
import ntpath
import os
import glob
import uuid
import base64

# get list of all subfile paths from src_path
def get_file_paths(src_path):
    file_paths = []
    for file_path in glob.glob(src_path + "*.*"):
        file_paths.append(file_path)
    return file_paths


# get list of all subfile names from src_path
def get_file_names(src_path):
    file_names = []
    file_paths = self.get_file_paths(src_path)
    for file_path in file_paths:
        file_name = self.path_leaf(file_path)
        file_names.append(file_name)
    return file_names



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
        return None 
    


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




