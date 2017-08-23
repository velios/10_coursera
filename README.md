# Coursera Dump

The program collects data from N courses in [Coursera](https://www.coursera.org) and saves the received data to a file

### How to Install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

### How to use
```bash
#Run
$ python3 coursera.py -n 5 -f out.xlsx
#Sample output
INFO:root:Script start fetch data from 5 courses ...
INFO:root:fetching https://www.coursera.org/learn/astro ...
INFO:root:fetching https://www.coursera.org/learn/developpement-durable ...
INFO:root:fetching https://www.coursera.org/learn/tesol-speaking ...
INFO:root:fetching https://www.coursera.org/learn/entender-diseno ...
INFO:root:fetching https://www.coursera.org/learn/positive-psychology-project ...
The program recorded data from 5 random courses on Coursera.org into file out.xlsx
```
Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.

# Project Goals

This README made with [Dilinger](http://dillinger.io/)
The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
