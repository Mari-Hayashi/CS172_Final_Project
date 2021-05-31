import os
import argparse

def BulkUpload(index_name, json_file):
    command = f"curl -X POST -u elastic:WLBCezXn0g7t6xNdzPclj0ke \"https://cs172-vrm.es.us-west1.gcp.cloud.es.io:9243/{index_name}/_bulk\" -H \"Content-Type: application/json\" --data-binary @{json_file}.json"
    os.system(command)

def GetNames():
    parser = argparse.ArgumentParser()

    parser.add_argument('index')
    parser.add_argument('json')
    args = parser.parse_args()
    BulkUpload(args.index, args.json)

def main():
    GetNames()

main()