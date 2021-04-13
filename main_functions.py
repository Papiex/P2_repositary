from functions import find_info_book, search_books_links_cat

import csv

import requests
from bs4 import BeautifulSoup 


def all_category_links():
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


def writing_to_csv(name_csv):
    """with name_csv as name, writing a csv in writing mode"""

    with open(name_csv + ".csv", "w", encoding="utf-8") as f:

        colums_name = [
            "[product_page_url]",
            "[upc]",
            "[title]",
            "[price_including_tax]",
            "[price_excluding_tax]",
            "[number_available]",
            "[product_description]",
            "[category]",
            "[review_rating]",
            "[img_url]"
        ]

        writer = csv.DictWriter(f, fieldnames=colums_name, delimiter="\t")
        writer.writeheader()


def append_to_csv(cat_names, name_cat):
    """call the function search_books_links_cat() who go search for all links in the dict {cat_names} with the key variable (name_cat)
    and return a list [book_links] and for all url in, we call the function find_info_book() who return "book info" in a list [info] and write this list in append mode to the
    current key variable (name_cat".csv") """

    for link in cat_names[name_cat]:
        books_links = search_books_links_cat(link)

        for book_link in books_links:
            info = find_info_book(book_link)

            with open(name_cat + ".csv", "a", encoding="utf-8") as f:

                colums_name = [
                    "[product_page_url]",
                    "[upc]",
                    "[title]",
                    "[price_including_tax]",
                    "[price_excluding_tax]",
                    "[number_available]",
                    "[product_description]",
                    "[category]",
                    "[review_rating]",
                    "[img_url]"
                ]

                writer = csv.DictWriter(
                    f, fieldnames=colums_name, delimiter="\t")
                writer.writerow({
                    "[product_page_url]": book_link,
                    "[upc]": info[0],
                    "[title]": info[5],
                    "[price_including_tax]": info[1],
                    "[price_excluding_tax]": info[2],
                    "[number_available]": info[3],
                    "[product_description]": info[6],
                    "[category]": info[4],
                    "[review_rating]": info[8],
                    "[img_url]": info[7]
                })


def split_name_category(link):
    """
    Split on underscore for return name category
    """

    link = link.split("_")[0]
    link = link.replace(
        "http://books.toscrape.com/catalogue/category/books/", "")
    return link