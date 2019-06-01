#!/usr/bin/env python3
import os
import sys
import json
import csv

import pylint_parser
import bandit_parser

# all of the information associated with a file
class BothInfo:
    def __init__(self, 
                filename : str, 
                pylint_info : pylint_parser.PylintInfo,
                bandit_info : bandit_parser.BanditInfo):
        self.pylint_info = pylint_info
        self.bandit_info = bandit_info
        self.filename = filename 
        
def combine(pylint_dict, bandit_dict):
    intersection_dict = dict()
    for filename in pylint_dict:
        pylint_info = pylint_dict[filename]
        if filename in bandit_dict:
            bandit_info = bandit_dict[filename]
            intersection = BothInfo(filename, pylint_info, bandit_info)
            intersection_dict[filename] = intersection
        else:
            continue
    return intersection_dict

def intersect_lines(intersection_dict, output_dir):
    # find an pylint message that report the same line as bandit reports
    # output to a csv file
    with open(output_dir + 'intersect_lines.csv', 'w') as outputcsv:
        fieldnames = ['filename', 'line_number', 
                        'pylint_message', 'pylint_type', 'pylint_symbol',
                        'bandit_issue_text', 'bandit_issue_confidence', 'bandit_issue_severity']
        csv_writer = csv.DictWriter(outputcsv, fieldnames=fieldnames)
        csv_writer.writeheader()
        for filename in intersection_dict:
            pylint_info = intersection_dict[filename].pylint_info
            bandit_info = intersection_dict[filename].bandit_info
            for pylint_msgs in pylint_info.all_msgs:
                for pylint_msg in pylint_msgs:
                    for res in bandit_info.result_list:
                        if res['line_number'] == pylint_msg.line:
                            csv_writer.writerow({   'filename'                  : filename,
                                                    'line_number'               : pylint_msg.line,
                                                    'pylint_message'            : pylint_msg.message,
                                                    'pylint_type'               : str(pylint_msg.category),
                                                    'pylint_symbol'             : pylint_msg.symbol,
                                                    'bandit_issue_text'         : res['issue_text'],
                                                    'bandit_issue_confidence'   : res['issue_confidence'],
                                                    'bandit_issue_severity'     : res['issue_severity']})


def main():
    # Usage: ./main.py <input_path> <output_path>
    # there files will be generated:
    # include '/' at the end
    #       <output path>bandit.json
    #       <output path>pylint.json
    #       <output path>intersect_lines.csv
    if len(sys.argv) != 3:
        print("Usage: ./main.py <path to the code to be analyzed> <output path>")
        sys.exit()
    
    pylint_dict = pylint_parser.process_all(sys.argv[1], sys.argv[2])
    bandit_dict = bandit_parser.process_all(sys.argv[1], sys.argv[2])
    intersection_dict = combine(pylint_dict, bandit_dict)
    for filename in intersection_dict:
        print(filename)
    intersect_lines(intersection_dict,  sys.argv[2])

if __name__ == "__main__":
    main()
