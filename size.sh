#!/bin/bash

#unzip '*.zip'
#for x in *.tar.gz; do tar -xvzf $x; done
#for x in *.tar.bz2; do tar -xvjf $x; done

#gets size of each directory
for d in */ ; do
    t=${d%?}
    #echo "running getting size of $t"
    SIZE="$(du -s $t | cut -d$'\t' -f 1)"
    echo "$t,$SIZE"
done
