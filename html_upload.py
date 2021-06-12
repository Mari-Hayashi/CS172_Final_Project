import argparse
import zipfile
from bs4 import BeautifulSoup
import os

def FormatString(string):
    return string.replace('\"', "\\\"").replace('\n', '').encode("ascii", errors="ignore").decode()

def ExtractHtmls(zip_folder_name, names_text_file):
    filename_to_link_map = {}
    with open(names_text_file) as f:
        lines = f.readlines()
        for line in lines:
            tokens = line.split(' ')
            filename_to_link_map[tokens[0]] = FormatString(tokens[1])
        
    with zipfile.ZipFile(f"{zip_folder_name}.zip", 'r') as zip_ref:
        zip_ref.extractall()
    # Retrieve the names of all html files
    for dir_path, dir_names, file_names in os.walk(zip_folder_name):
        allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store" and filename[len(filename) - 5:] == ".html")]

    contents = []
    for file in allfiles:
        with open(file, 'r', encoding='ISO-8859-1') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            if soup.title is not None and soup.title.string is not None: # If this is html
        
                # if windows
                if os.name == "nt":
                    filename = file[2 * len(zip_folder_name) + 2:] 

                # if non-windows
                else:
                    filename = file[len(zip_folder_name) + 1:]
                if filename not in filename_to_link_map:
                    print(f"Warning! The file {filename} is missing link information in {names_text_file}. Skipping this file.")
                    continue
                content = {
                    "title": FormatString(soup.title.string),
                    "body": FormatString(soup.get_text()),
                    "link": filename_to_link_map[filename]
                }
                contents.append(content)
    return contents

parser = argparse.ArgumentParser()

parser.add_argument("html_folder")
parser.add_argument("filenames")
parser.add_argument('index_name')
args = parser.parse_args()

html_contents = ExtractHtmls(args.html_folder, args.filenames)

file_index = 1
file_name = "bulk_file_" + str(file_index)
while os.path.isfile(file_name):
    file_index += 1
    file_name = "bulk_file_" + str(file_index)
    
with open(f'{file_name}.json', 'w', encoding="utf-8") as output_file:
    for content in html_contents:
        output_file.write("{\"index\":{}}\n")
        output_file.write("{ \"title\":\"" + content["title"] + "\", \"body\":\"" + content["body"] + "\", \"link\":\"" + content["link"] + "\"}\n")

create_index_command = f"curl -X PUT -u elastic:WLBCezXn0g7t6xNdzPclj0ke https://cs172-vrm.es.us-west1.gcp.cloud.es.io:9243/{args.index_name}"
os.system(create_index_command)
upload_files_command = f"curl -X POST -u elastic:WLBCezXn0g7t6xNdzPclj0ke \"https://cs172-vrm.es.us-west1.gcp.cloud.es.io:9243/{args.index_name}/_bulk\" -H \"Content-Type: application/json\" --data-binary @{file_name}.json"
os.system(upload_files_command)
