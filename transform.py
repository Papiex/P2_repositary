import os
import time
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from extract import get_response_of_book


def find_info_book(link_of_book: str):
    """Search in link_of_book content and transform into required info"""

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
    # if response not ok 
    elif no_response == True:
        for _ in range(10):
            info.append("No response for this book")

    return info


def get_index_info(tr_list: List[str]):
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


def split_name_category(link: str):
    """Split on underscore for return name category and transform like this historical-fiction => Historical Fiction"""

    link = link.split("_")[0]
    link = link.replace(
        "http://books.toscrape.com/catalogue/category/books/", "")
    link = link.capitalize().replace("-"," ").title()
    return link