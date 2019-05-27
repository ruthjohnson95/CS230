# CS230 - Term Project

### Dependencies
In order to run our scripts, the following packages need to be installed:
- Python2.7
    - install with `apt-get install python`
- Bandit
    - install with `pip install bandit`
- PyLint
    - install with `apt-get install pylint`

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

### Build the Final Report to PDF 
The final report is written in LaTex and can be built into pdf file by running the following command inside `doc/` directory:
```
make
```
