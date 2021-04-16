import os
import time

import requests
from bs4 import BeautifulSoup


def find_info_book(link_of_book):
    """With link_of_book as value search and extract required info and return them"""

    info = []
    response = requests.get(link_of_book)
    soup = BeautifulSoup(response.content, "lxml")
    names_list = [
        "UPC",
        "Price (excl. tax)",
        "Price (incl. tax)",
        "Availability"]
    names_compare = soup.find_all("tr")
    info = compare(names_list, names_compare)
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
        print("no description for " + link_of_book)
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

    return info


def compare(names_list, names_compare):
    """Compare two list and append if the result is the same"""

    info = []

    if names_list[0] in names_compare[0].th:
        universal_product_code = names_compare[0].find("td").text
        info.append(universal_product_code)

    else:
        print("UPC not in compare list[0]")

    if names_list[1] in names_compare[2].th:
        price_excluding_tax = names_compare[2].find("td").text
        info.append(price_excluding_tax)

    else:
        print("Price (excl. tax) not in compare list[2]")

    if names_list[2] in names_compare[3].th:
        price_including_tax = names_compare[3].find("td").text
        info.append(price_including_tax)

    else:
        print("Price (incl. tax) not in compare list[3]")

    if names_list[3] in names_compare[5].th:
        Availability = names_compare[5].find("td").text
        info.append(Availability)

    else:
        print("Availability not in compare list[5]")

    return info


def split_name_category(link):
    """Split on underscore for return name category"""

    link = link.split("_")[0]
    link = link.replace(
        "http://books.toscrape.com/catalogue/category/books/", "")
    return link
