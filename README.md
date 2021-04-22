# Script of scraping

#### This script scrap [book.toscrape.com](http://books.toscrape.com/) (fake site of books store) and extract and store all books data of each category in csv files :

- Create one main folder named "csv files" which will contain all data

- For each category on the site, create one folder accorded with name of the current scraping category

- In this folder, he create also a folder named "jpg files" who contains books pictures

- Always in the same folder, he write and create a csv file who contains all books data

#### List of data extracted :

- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

*See below for a demonstration*

## Requirements
This script is write with Python 3 and require minimum :
```bash
Python 3.x.x
```
## Installation on Windows
__1- You need to create virtual env with this command :__

*The virtual env is installed in the directory where you are (the path) with your terminal*

- ```python -m venv env```

__2- Now you have to activate your virtual env, the default path is :__
- if you use PowerShell :
``` env/Scripts/activate.ps1```
- if you use CMD or terminal that supports __.bat__ :
``` env/Scripts/activate.bat```

## Installation on Linux
__1- You need to create virtual env with this command :__

*The virtual env is installed in the directory where you are (the path) with your terminal*

- ```python -m venv env```

__2- Now you have to activate your virtual env, the default path is :__
``` source env/bin/activate```

## Installation on Mac
__1- You need to create virtual env with this command :__

*The virtual env is installed in the directory where you are (the path) with your terminal*

- ```python -m venv env```

__2- Now you have to activate your virtual env, the default path is :__
``` source env/bin/activate```

## Libraries
__This program need some libraries, for installing them, use this command (in your virtual env) :__

*View requirements.txt to know which library/version is used*

- ```pip install -r requirements.txt```

## Launch the script
Enter this command in your virtual env :

- ```py main.py```

## Demonstration with "TRAVEL" category :

__1- At the beginning, a folder named "csv files" is created there where you have launched main.py :__

*main folder*
![image](https://user-images.githubusercontent.com/81369778/115397209-23cb2d00-a1e6-11eb-87f3-48069d8af89c.png)

__2- Now writing and downloading pictures for category "TRAVEL" on book.toscrape.com in progress :__

*We can see the numbers of books extracted in real time*

![image](https://user-images.githubusercontent.com/81369778/115397526-7d335c00-a1e6-11eb-98e5-0e01d500952d.png)

__3- At the same time, a folder is created and named according to the current category (TRAVEL in this case) :__

*csv files folder*
![image](https://user-images.githubusercontent.com/81369778/115392756-3858f680-a1e1-11eb-9a85-1f0dde46bc60.png)

__-4 In this folder (TRAVEL), 2 files are created :__
- __"jpg files"__ (who contains pictures of the current category)
- A csv file named according to the current category

*Travel folder*
![image](https://user-images.githubusercontent.com/81369778/115380590-03de3e00-a1d3-11eb-94eb-434f6b4888e9.png)


__-5 When he's finish one category we can know how much time has elapsed for scraping this category also the numbers of books extracted :__

![image](https://user-images.githubusercontent.com/81369778/115394962-a3a3c800-a1e3-11eb-9caa-d9c61c774d50.png)

__-6 Here is the CSV file after writing of the category "Travel"__

__The last column [img_names] matches with names of pictures in the folder "jpg files" of this category__

*jpg files*
![image](https://user-images.githubusercontent.com/81369778/115380638-10fb2d00-a1d3-11eb-8458-8e640861bd68.png)
*travel.csv*
![image](https://user-images.githubusercontent.com/81369778/115381025-74855a80-a1d3-11eb-8528-db5bdd29fe17.png)

__This operation will be repeated as many times as the number of category of the site__
