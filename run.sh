#!/bin/bash

# step 1: move all the benchmarks you want to test into a directory of your choice
# step 2: cd into that directory
# step 3: make directories for bandit ouput files and pyline output files (they may be the same directory) 
# step 4: run script as path/to/run.sh [path of bandit_to_csv.py] [path of pylint_to_csv.py] [directory to dump bandit output] [directory to dump pylint output]
#       i.e.  ../CS230/run.sh "../CS230/bandit parser/bandit_to_csv.py" ../CS230/pylint_to_csv.py bandit_output pylint_output

if [ "$#" -ne 4 ]; then
    echo "Need all 4 arguments"
    exit 1
fi

#decompresses all python packages
unzip '*.zip'
for x in *.tar.gz; do tar -xvzf $x; done
for x in *.tar.bz2; do tar -xvjf $x; done

for d in */ ; do
    t=${d%?}
    if [ "$t" = "$3" ] || [ "$t" = "$4" ] || [ "$d" = "$3" ] || [ "$d" = "$4" ]; then
        continue
    fi
    python3 "$1" $t --out $t
    python3 "$2" $t $t
done

mv *_bandit.txt "$3"
mv *_pylint.txt "$4"
