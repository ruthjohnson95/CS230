# CS230 - Term Project

### Dependencies
In order to run our scripts, the following packages need to be installed:
- Python2.7
    - install with `apt-get install python`
- Bandit
    - install with `pip install bandit`
- PyLint
    - install with `apt-get install pylint`
- Pandas
    - install with `pip3 install pandas` or `pip install pandas`
    
### How to run Bandit on a benchmark (you don't need docker for this)
1) Download this git repository, "CS230" (or git pull to get the latest changes, if you've already downloaded it - this step does NOT need to be repeated for each benchmark)
2) Download a benchmark from our CS230-Benchmarks Google Drive (for example, "aiocouchdb-0.5.0") and unzip it inside the "CS230" folder on your local machine
3) Make sure you have a Terminal open in the "CS230" folder on your local machine
4) In Terminal, run the following command, but replace "aiocouchdb-0.5.0" with the name of the benchmark 
```
$ python 'bandit parser/bandit_to_csv.py' aiocouchdb-0.5.0 --out aiocouchdb-0.5.0
```
5) In your local CS230 folder, you will now find a file called aiocouchdb-0.5.0_bandit.txt. Put that file into our Bandit_output folder: https://drive.google.com/drive/folders/1aPIXtjPLKlbuTkmBAgzo1Aw3-Gkffz_R?usp=sharing

### How to run Pylint on a benchmark (you need docker)
1) If you just downloaded (or git pulled) this "CS230" repository with latest changes, you need to run the docker build command below. Otherwise, this step does NOT need to be repeated for each benchmark.
```
$ docker build --tag=cs230 .
```
2) Run a bash shell inside docker container:
```
$ docker run -it cs230 bash
```
Your terminal will now say something like: root@aa7885c90033:/CS230-Term-Project#

3) Assuming you already downloaded the benchmark for Bandit, open up another Terminal window and run this command to copy the benchmark into your docker container: (but replace "aiocouchdb-0.5.0" with the name of the benchmark , and replace "aa7885c90033" with whatever it says in your docker container in the other terminal window)
```
$ docker cp aiocouchdb-0.5.0 aa7885c90033:/CS230-Term-Project/
```
4) Go back to the Terminal window with the docker container. Change directories into the benchmark directory:
```
$ cd aiocouchdb-0.5.0
```
5) In that docker terminal, run the following command, but replace "aiocouchdb-0.5.0" with the name of the benchmark :
```
$ python3 ../pylint_to_csv.py . aiocouchdb-0.5.0
```
6) Open a new Terminal window. Copy the generated output file (in our example, aiocouchdb-0.5.0_pylint.txt) to Desktop (or wherever else you want on your local machine):
```
$ docker cp aa7885c90033:/CS230-Term-Project/aiocouchdb-0.5.0/aiocouchdb-0.5.0_pylint.txt ~/Desktop
```
7) Put that file into our Pylint_output folder: https://drive.google.com/drive/folders/1DLiYPP594fUsGQsNAM5lU_b_-xQ2xxvg?usp=sharing
8) Put the name of the benchmark you just analyzed into our benchmark spreadsheet: https://docs.google.com/spreadsheets/d/1ksNLVrU66Kg44QzC44GvuiZCx4mmXIzWSkgNYsWpHrM/edit?usp=sharing

### Using Docker
We provide a Dockerfile that contains all of the dependencies you need to run the scripts. 

To build the docker image, run the following command inside the repository directory:
```
$ docker build --tag=cs230 .
```

Confirm that the image exists after building:
```
$ docker image ls
```

To run the script inside the docker container:
```
$ docker run cs230
```

To run a bash shell inside of docker container:
```
$ docker run -it cs230 bash
```

### Build the Final Report to PDF 
The final report is written in LaTex and can be built into pdf file by running the following command inside `doc/` directory:
```
make
```
