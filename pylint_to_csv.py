#!/usr/bin/env python3

# To run: go into directory of project, then: python3 /path/to/pylint_to_csv.py . directory_name

import os
import sys
import json
import pandas as pd

from enum import Enum

class PylintInfo:
    """A data structure for holding pylint info about a filename

    Inputs:
    -------
    filename : String
        the filename name of this object
    """
    def __init__(self, 
                filename: str):
        self.filename = filename
        # each PylintInfo object has lists of messages 
        self.I_msgs = [] # [I]nformational messages that Pylint emits (do not contribute to your analysis score)
        self.R_msgs = [] # [R]efactor for a "good practice" metric violation
        self.C_msgs = [] # [C]onvention for coding standard violation
        self.W_msgs = [] # [W]arning for stylistic problems, or minor programming issues
        self.E_msgs = [] # [E]rror for important programming issues (i.e. most probably bug)
        self.F_msgs = [] # [F]atal for errors which prevented further processing

    def add_Imsg(self, imsg):
        self.I_msgs.append(imsg)

    def add_Rmsg(self, rmsg):
        self.R_msgs.append(rmsg)

    def add_Cmsg(self, cmsg):
        self.C_msgs.append(cmsg)

    def add_Wmsg(self, wmsg):
        self.W_msgs.append(wmsg)

    def add_Emsg(self, emsg):
        self.E_msgs.append(emsg)

    def add_Fmsg(self, fmsg):
        self.F_msgs.append(fmsg)

    def count_total(self):
        return (len(self.I_msgs)+
                len(self.W_msgs)+ 
                len(self.E_msgs)+ 
                len(self.C_msgs)+ 
                len(self.F_msgs)+ 
                len(self.R_msgs))

    def count(self, attr: str, tgt: str):
        return (sum(1 for i in self.I_msgs if getattr(i, attr)==tgt) + 
                sum(1 for i in self.R_msgs if getattr(i, attr)==tgt) + 
                sum(1 for i in self.W_msgs if getattr(i, attr)==tgt) + 
                sum(1 for i in self.C_msgs if getattr(i, attr)==tgt) + 
                sum(1 for i in self.E_msgs if getattr(i, attr)==tgt) + 
                sum(1 for i in self.F_msgs if getattr(i, attr)==tgt))

    def __str__(self):
        s = "\n=============\n"
        s +="I messages:\n"
        for i in self.I_msgs:
            s += str(i)
        s += "\n"
        s +="R messages:\n"
        for i in self.R_msgs:
            s += str(i)
        s += "\n"
        s +="W messages:\n"
        for i in self.W_msgs:
            s += str(i)
        s += "\n"
        s +="C messages:\n"
        for i in self.C_msgs:
            s += str(i)
        s += "\n"
        s +="E messages:\n"
        for i in self.E_msgs:
            s += str(i)
        s += "\n"
        s +="F messages:\n"
        for i in self.F_msgs:
            s += str(i)
        s += "\n"
        return s

class Category(Enum):
    I = 1
    R = 2
    C = 3
    W = 4
    E = 5
    F = 6

type2category_map = {
    "convention"    : Category.C,
    "warning"       : Category.W,
    "error"         : Category.E,
    "refactor"      : Category.R,
    "fatal"         : Category.F,
    "info"          : Category.I
}

class Message:
    """A Pylint Message"""
    def __init__(self, 
                category    : Category, 
                message     = "", 
                obj         = "", 
                module      = "",
                symbol      = "",
                line        = -1,
                column      = -1):
        # the type of the message, see above
        self.category = category
        # the message body
        self.message = message
        # the object (either a function or a class) name within the module
        self.obj = obj
        # module name
        self.module = module
        # symbolic name of the message (eg. locally-disabled)
        self.symbol = symbol
        # line number
        self.line = line
        # column number
        self.column = column

    def __str__(self):
        return ("{\n"+
            "\tcategory = " + str(self.category) + ",\n" +
            "\tmessage = " + self.message + ",\n" +
            "\tobj = " + self.obj + ",\n" +
            "\tmodule = " + self.module + ",\n" +
            "\tsymbol = " + self.symbol + ",\n" +
            "\tline = " + str(self.line) + ",\n" +
            "\tcolumn = " + str(self.column) + ",\n" + 
            "}\n")

def process_all(dir):
    all_info = dict()
    os.system("find "+dir+" -iname \"*.py\" | xargs pylint --output-format=json --files-output=y")
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".json"):
                pylint_info = parse(file)
                all_info[pylint_info.filename] = pylint_info
    
    if os.stat("pylint_global.json").st_size == 0:
        return all_info

    with open('pylint_global.json', "r") as f:
        msg_list = json.load(f)
        for msg_dic in msg_list:
            t = msg_dic['type']

            if msg_dic['module'] in all_info:
                pylint_info = all_info[msg_dic['module']]
            else:
                pylint_info = PylintInfo(msg_dic['module'])
                all_info[msg_dic['module']] = pylint_info
            
            msg = Message(
                category=type2category_map[t],
                message=msg_dic['message'],
                obj=msg_dic['obj'],
                module=msg_dic['module'],
                symbol=msg_dic['symbol'],
                line=msg_dic['line'],
                column=msg_dic['column'])
            if msg.category==Category.I:
                pylint_info.add_Imsg(msg)
            elif msg.category==Category.E:
                pylint_info.add_Emsg(msg)
            elif msg.category==Category.F:
                pylint_info.add_Fmsg(msg)
            elif msg.category==Category.C:
                pylint_info.add_Cmsg(msg)
            elif msg.category==Category.R:
                pylint_info.add_Rmsg(msg)
            elif msg.category==Category.W:
                pylint_info.add_Wmsg(msg)
            else:
                raise Exception("Message category undefined")
    return all_info

def parse(filename: str): 
    """parse Pylint on this given file

    Inputs
    ------
    filename : String
                the name of the file to be ran on

    Returns
    -------
    pylint_info : PylintInfo
                    a data structure that captures all of the 
                    information from pylint
    """
    pylint_info = PylintInfo(filename[7:-5])
    if os.stat(filename).st_size == 0:
        return pylint_info
    with open(filename) as f:
        msg_list = json.load(f)
        for msg_dic in msg_list:
            t = msg_dic['type']
            msg = Message(
                category=type2category_map[t],
                message=msg_dic['message'],
                obj=msg_dic['obj'],
                module=msg_dic['module'],
                symbol=msg_dic['symbol'],
                line=msg_dic['line'],
                column=msg_dic['column'])
            if msg.category==Category.I:
                pylint_info.add_Imsg(msg)
            elif msg.category==Category.E:
                pylint_info.add_Emsg(msg)
            elif msg.category==Category.F:
                pylint_info.add_Fmsg(msg)
            elif msg.category==Category.C:
                pylint_info.add_Cmsg(msg)
            elif msg.category==Category.R:
                pylint_info.add_Rmsg(msg)
            elif msg.category==Category.W:
                pylint_info.add_Wmsg(msg)
            else:
                raise Exception("Message category undefined")
    return pylint_info
                
## Test ##
def main():
    dic=process_all(sys.argv[1])
    counts = dict()
    for key in dic:
        counts[key] = {
            "I":len(dic[key].I_msgs),
            "R":len(dic[key].R_msgs),
            "C":len(dic[key].C_msgs),
            "W":len(dic[key].W_msgs),
            "E":len(dic[key].E_msgs),
            "F":len(dic[key].F_msgs),
        }

    # Process to make it into csv format
    # df = pd.Series(dic).to_frame()
    df = pd.DataFrame.from_dict(counts, orient='index', columns=['I','R','C','W','E','F'])

    out_prefix = sys.argv[2] 
    out_fname = out_prefix + "_pylint.txt"
    print("Outputing results of pylint to: %s" % out_fname)
    df.to_csv(out_fname, index=False)
    
if __name__ == "__main__":
    main()
