import requests
from bs4 import BeautifulSoup 



def search_books_links_cat(category_link):
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


def picture_download(img_link, name_cat, number):
    """download picture with this path => name_cat/jpg files/Picture_number.png"""
    
    response = requests.get(img_link)
    file = open("csv files/" + name_cat + "/jpg files/" + "Picture_" + str(number) + ".jpg" , "wb")
    file.write(response.content)
    file.close()
