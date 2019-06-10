# CS230 - Term Project

## How to run our code:
1) Run `git clone https://github.com/ruthjohnson95/CS230.git` to clone a local version of our repository.
    
2) Make a directory (preferably not in the local repository) to
hold all the Python packages you want to test. Change the current working directory to this directory. All the following commands will be run from this directory.

3) Make a directory under the above directory as a place to store all the output files after processing is finished (i.e. `mkdir output`).

4) Copy `insecure_full.json` from `insecure_libraries/download_script` to the current directory (or create your own custom json in the same format). This will determine what packages will be downloaded and tested.

5) Run `python3 [path to local repo]/insecure_libraries/download_script/parse_insecure.py` to parse the json file and download the packages. (i.e. `../CS230/insecure_libraries/download_script/parse_insecure.py`).

6) Either install bandit (`pip3 install bandit`) and pylint (`pip3 install pylint`) to run these tools locally, or install docker (`sudo apt-get install docker`) to run everything in our docker container.

7) Run `[path to local repo]/run.sh [path to local repo] [path of some directory to dump output] [True/False on whether you want to run using docker]` to run our tests on all the packages that have been downloaded (i.e. `../CS230/run.sh ../CS230 output`). 

8) Run `[path to local repo]/size.sh` to get a file with the size (in kilobytes) of all the benchmarks (i.e. `../CS230/size.sh`). This may be used to normalize the number of Bandit vulnerabilities and Pylint issues for packages of different sizes.
