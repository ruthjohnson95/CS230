import os
import sys
import json

from enum import Enum

class BanditInfo:
    def __init__(self, filename: str):
        self.filename = filename 
        self.result_list = []
    
    def add_result(self, result):
        # result is a dictionary extracted from the json file
        self.result_list.append(result)
    
def process_all(input_dir, output_dir):
    all_info = dict()
    os.system("bandit -f json -r " + input_dir + " > " + output_dir + "bandit.json")
    try:
        fh = open(output_dir + "bandit.json", 'r')
    except FileNotFoundError:
        print("No JSON file generated, quit")
        return all_info

    if os.stat(output_dir + "bandit.json").st_size == 0:
        return all_info
    
    with fh as f:
        all_bandit_output = json.load(f)
        results = all_bandit_output['results']
        for res in results:
            filename = res['filename']
            if filename in all_info:
                bandit_info = all_info[filename]
            else:
                bandit_info = BanditInfo(filename)
                all_info[filename] = bandit_info
            bandit_info.add_result(res)

    return all_info
