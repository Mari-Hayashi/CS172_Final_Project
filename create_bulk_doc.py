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
        print(f"Found {len(file_names)} html files!")
        allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store" and filename[len(filename) - 5:] == ".html")]
    contents = []
    for file in allfiles[0:]:
        with open(file, 'r', encoding='ISO-8859-1') as f:
            filename = file[len(zip_folder_name) + 1:]
            if filename not in filename_to_link_map:
                print(f"Warning! The file {filename} is missing link information in {names_text_file}. Skipping this file.")
                continue
            soup = BeautifulSoup(f.read(), 'html.parser')
            content = {
                "title": FormatString(soup.title.string),
                "body": FormatString(soup.get_text()),
                "link": filename_to_link_map[filename]
            }
            contents.append(content)
    return contents

parser = argparse.ArgumentParser()

parser.add_argument("input")
parser.add_argument("filenames")
parser.add_argument("output")
args = parser.parse_args()

html_contents = ExtractHtmls(args.input, args.filenames)

with open(args.output + '.json', 'w', encoding="utf-8") as output_file:
    for content in html_contents:
        output_file.write("{\"index\":{}}\n")
        output_file.write("{ \"title\":\"" + content["title"] + "\", \"body\":\"" + content["body"] + "\", \"link\":\"" + content["link"] + "\"}\n")