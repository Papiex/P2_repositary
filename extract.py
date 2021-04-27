import time
from typing import List
from urllib.error import HTTPError

from transform import split_name_category

import requests
from bs4 import BeautifulSoup


def search_books_links_category(category_link: str) -> List[str]:
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
    books_links.append("http://books.toscrape.com/catalogue/a-light-in-the-attic_1001/index.html")
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


def download_picture(image_link: str, name_category: str, image_number: int) -> None:
    """download picture with this path => name_category/jpg files/Picture_number.png"""

    response = requests.get(image_link)
    file = open("csv files/" + name_category + "/jpg files/" + "Picture_" + str(image_number) + ".jpg" , "wb")
    file.write(response.content)
    file.close()


def get_response_of_book(link_of_book: str) -> bool:
    """
    print n° of error if requests have no response and return True or False 
    ( for skip this url book in append_to_csv() )
    """

    response = requests.get(link_of_book)

    if response.ok:
        soup = BeautifulSoup(response.content, "lxml")
        no_response = False


    else:
        print("Something wrong with " + link_of_book)
        print("Error n° " + str(response.status_code))
        time.sleep(1)
        print("Skipping to the next book...")
        time.sleep(1)
        no_response = True
        soup = None
    return soup, no_response


def find_info_book(link_of_book: str) -> List[str]:
    """Search in link_of_book content and extract required info"""

    info = []
    soup, no_response = get_response_of_book(link_of_book)
    # if response ok
    if no_response == False:
        tr_list = soup.find_all("tr")
        info = get_index_info(tr_list)

        category_search = soup.find(class_="breadcrumb")
        category_book = category_search.find_all("a")
        category = category_book[2]
        info.append(category.text)

        titles = soup.find("h1").text
        info.append(titles)

        # Some books have no description, with this, if book have no description,
        # replace description by ("This book have no description")
        try:
            confirm_description = soup.find(
                id="product_description").find("h2").text

            if confirm_description == "Product Description":
                description = soup.find("h2").find_next().text

        except AttributeError:
            description = ("This book have no description")
            pass

        info.append(description)

        img_src = soup.find_all("img")[0].get("src")
        img_id = img_src.split("cache")[1]
        img_link = f"http://books.toscrape.com/media/cache{img_id}"
        info.append(img_link)

        star_rating = soup.find_all("p", class_="star-rating")[0].get("class")
        # Search the note and remove "star-rating" if classes come to be in the
        # wrong order in index list.
        if "star-rating" in star_rating:
            star_rating.remove("star-rating")
            info.append(star_rating[0])
    # if response not ok ################
    else:
        pass

    return info, no_response


def get_index_info(tr_list: List[str]) -> List[str]:
    """Try to transform and append required info from list, if dont find replace by (No ... found for this book)"""

    info = []

    try:
        universal_product_code = tr_list[0].find("td").text

    except IndexError:
        universal_product_code = "No UPC found for this book"
        pass

    try:
        price_excluding_tax = tr_list[2].find("td").text

    except IndexError:
        price_excluding_tax = "No price_excl_tax found for this book"
        pass

    try:
        price_including_tax = tr_list[3].find("td").text

    except IndexError:
        price_including_tax = "No price_incl_tax found for this book"
        pass

    try:
        Availability = tr_list[5].find("td").text

    except IndexError:
        Availability = "No Availability found for this book"
        pass

    info.append(universal_product_code)
    info.append(price_excluding_tax)
    info.append(price_including_tax)
    info.append(Availability)

    return info