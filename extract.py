import time
from typing import List
from urllib.error import HTTPError

import requests
from bs4 import BeautifulSoup


def search_books_links_category(category_link: str):
    """ with values as category_link, return all books links of category_link in a list """

    books_links = []
    url = category_link
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.content, "lxml")
        info_book_url = soup.find_all(
            class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        for h3 in info_book_url:

            a = h3.find("a")
            book_link = a["href"].replace("../../../", "")
            books_links.append(
                "http://books.toscrape.com/catalogue/" + book_link)

    return books_links


def get_all_category_links() -> List[str]:
    """ Search and return all category urls and return them in a list """

    category_links = []
    url = "http://books.toscrape.com/index.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    nav = soup.find(class_="nav nav-list")
    nav1 = nav.find("li")
    nav2 = nav1.find("ul")
    navs = nav2.find_all("li")

    for li in navs:

        a = li.find("a")
        category_link = a["href"]
        category_linky = ("http://books.toscrape.com/" + category_link)
        category_links.append(category_linky)

    return category_links


def download_picture(image_link: str, name_category: str, image_number: int):
    """download picture with this path => name_category/jpg files/Picture_number.png"""

    response = requests.get(image_link)
    file = open("csv files/" + name_category + "/jpg files/" + "Picture_" + str(image_number) + ".jpg" , "wb")
    file.write(response.content)
    file.close()


def get_response_of_book(link_of_book: str) -> bool:
    """
    With link_of_book as value search and extract required info and return them
    return True and content or False according to response.
    """

    response = requests.get(link_of_book)

    try:
        soup = BeautifulSoup(response.content, "lxml")
        no_response = False
        return soup, no_response
        
    except HTTPError as error_code:
        if error_code == 500:
            print("Internal Server Error 500 for" + "\n" + link_of_book)
            time.sleep(1)
            print("Skipping to the next book...")
            no_response = True
            return no_response
        else:
            print("Something went wrong Error code :" + "\n" + link_of_book + "\n" + error_code.code)
            time.sleep(1)
            print("Skipping to the next book...")
            no_response = True
            return no_response