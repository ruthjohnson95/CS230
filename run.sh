#!/bin/bash

# step 1: move all the benchmarks you want to test into a directory of your choice
# step 2: cd into that directory
# step 3: make directories for bandit ouput files and pyline output files (they may be the same directory) 
# step 4: run script as path/to/run.sh [path of git project] [directory to dump all output] [true or false on whether to run docker]
#       i.e. ../CS230/run.sh ../CS230 output/ true &> output/log.txt (if you want to dump output of this script to a file)

if [ "$#" -ne 3 ]; then
    echo "Need all 3 arguments"
    exit 1
fi

#decompresses all python packages
unzip '*.zip'
for x in *.tar.gz; do tar -xvzf $x; done
for x in *.tar.bz2; do tar -xvjf $x; done

#runs bandit first
for d in */ ; do
    t=${d%?}
    echo "running bandit on $t"
    if [ "$t" = "$2" ] || [ "$d" = "$2" ]; then
        continue
    fi

    python3 "$1/bandit parser/bandit_to_csv.py" $t --out $t
done
mv *_bandit.txt "$2"

#starts docker for pylint
if [ "$3" = "true" ] || [ "$3" = "True" ] || [ "$3" = "TRUE" ]; then
    #Uncomment the line below if you recently pulled new changes
    docker build --tag=cs230 "$1"
    docker run -t -d cs230 bash


    CONTAINER_ID="$(docker ps | sed -n '2p' | cut -d ' ' -f 1)"
  
    echo "$CONTAINER_ID"
  

    docker exec $CONTAINER_ID mkdir /CS230-Term-Project/output  
    for d in */ ; do
        t=${d%?}

        if [ "$t" = "$2" ] || [ "$d" = "$2" ]; then
            continue
        fi
        echo "running dockerized bandit on $t"
        
        echo "running dockerized pylint and intersection analysis on $t"
        docker exec $CONTAINER_ID mkdir "/CS230-Term-Project/output/${t}_intersection"
        #docker cp $t "$CONTAINER_ID:/CS230-Term-Project"
        #docker exec $CONTAINER_ID python3 "/CS230-Term-Project/bandit parser/bandit_to_csv.py" $t --out $t
        docker cp "$CONTAINER_ID:/CS230-Term-Project/${t}_bandit.txt" $2
        docker exec $CONTAINER_ID python3 /CS230-Term-Project/pylint_to_csv.py $t $t
        docker cp "$CONTAINER_ID:/CS230-Term-Project/${t}_pylint.txt" $2
        docker exec $CONTAINER_ID python3 /CS230-Term-Project/Intersection_analysis/main.py $d "/CS230-Term-Project/output/${t}_intersection_"
        docker cp "$CONTAINER_ID:/CS230-Term-Project/output/${t}_intersection_pylint.json" $2
        docker cp "$CONTAINER_ID:/CS230-Term-Project/output/${t}_intersection_bandit.json" $2
        docker cp "$CONTAINER_ID:/CS230-Term-Project/output/${t}_intersection_intersect_lines.csv" $2
    done

    docker stop $CONTAINER_ID
    echo "docker finished"
    exit 1

else
    #runs non docker version of pylint
    for d in */ ; do
        t=${d%?}

        if [ "$t" = "$2" ] || [ "$d" = "$2" ]; then
            continue
        fi

        echo "running pylint and intersection analysis on $t"
        python3 "$1/pylint_to_csv.py" $t $t
        python3 "$1/Intersection_analysis/main.py" $d "$2/${t}_intersection_"
    done
    mv *_pylint.txt "$2"
fi
