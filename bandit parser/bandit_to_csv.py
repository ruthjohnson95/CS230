# Usage: py bandit.py <targets...>
# targets: one or more files/directories to run bandit on

import csv
import subprocess
from subprocess import PIPE
import argparse
import pandas as pd

try:
    # for Python 2.x
    from StringIO import StringIO
except ImportError:
    # for Python 3.x
    from io import StringIO

try:
    # for Python 3.x
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

parser = argparse.ArgumentParser(description='Process specified project.')
parser.add_argument('targets', nargs='+')
parser.add_argument("--out", dest="out_prefix", required=True, help="output file prefix; should be name of github repo", type=str)
args = parser.parse_args()

# run bandit on the given input targets
# note: bandit does not check its input target and raise error when the target does not exist
# on the contrary, it only exit with code 1 when issues are detected (i.e. when bandit runs successfully)
# so do not attempt to check this subprocess, it will always raise a CalledProcessError
# when everything is fine
bandit_result = subprocess.run(["bandit", "-r", "-f", "csv"] + args.targets, stdout=PIPE, stderr=DEVNULL)

# prefix to be used to define output file
out_prefix = args.out_prefix

# convert bandit_result into dictionary format
csv_reader = csv.reader(StringIO(bandit_result.stdout.decode("utf-8")), delimiter=',')
csv_headers = next(csv_reader, None)
diagnosis = {}
for h in csv_headers:
    diagnosis[h] = []
for row in csv_reader:
    for h, v in zip(csv_headers, row):
        diagnosis[h].append(v)

# convert the line range from string to a list of indexes
line_range_list = []
for line_range in diagnosis['line_range']:
    line_range_list.append([int(str) for str in line_range[1:-1].split(',')])
diagnosis['line_range'] = line_range_list
# convert line number to integers
diagnosis['line_number'] = [int(str) for str in diagnosis['line_number']]

df = pd.DataFrame(diagnosis)

out_fname = out_prefix + "_bandit.txt"
print("Outputing results of bandit to: %s" % out_fname)
df.to_csv(out_fname, index=False)
