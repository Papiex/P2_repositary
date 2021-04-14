# Script of scraping
Script for scraping purpose on [book.toscrape.com](http://books.toscrape.com/)
## Requirements
```bash
Python 3.x.x
```
## Installation on Windows/Linux
__1- You need to create virtual env with this command :__

*The virtual env is installed in the directory where you are (the path) with your terminal*

```bash
python -m venv env
```

__2- Now you have to activate your virtual env, the default path is :__
- if you use PowerShell =>
``` env/Scripts/activate.ps1```
- if you use CMD or terminal that supports __.bat__ =>
``` env/Scripts/activate.bat```
- The command on linux =>
``` env/Scripts/activate```

__3- This program need some libraries, for installing them, use this command (in your virtual env) :__

*View requirements.txt to know which library/version is used*

```bash
pip install -r requirements.txt
```
## Launch the script
Enter this command in your virtual env :

```py main.py```
