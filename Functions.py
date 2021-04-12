import requests
from bs4 import BeautifulSoup
import csv
import time
import os

def find_info_book(link_of_book):
    """ with link_of_book as value, search and extract required info and return them """
          
    info = []
    response = requests.get(link_of_book)
    soup = BeautifulSoup(response.content, "lxml")
    Names_list = ["UPC", "Price (excl. tax)", "Price (incl. tax)", "Availability"]
    Names_compare = soup.find_all("tr")
    info = test(Names_list, Names_compare) 
    category_search = soup.find(class_="breadcrumb")
    category_book = category_search.find_all("a")
    category = category_book[2]
    info.append(category.text)

    titles = soup.find("h1").text
    info.append(titles)
    try:                 # Some books have no description, with this, if book have no description, replace description by ("This book have no description")
        confirm_description = soup.find(id="product_description").find("h2").text
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

    # Search the note and remove "star-rating" if classes come to be in the wrong order in index list.
    star_rating = soup.find_all("p", class_="star-rating")[0].get("class")
    if "star-rating" in star_rating:
        star_rating.remove("star-rating")
        info.append (star_rating[0])
    return info

def test(Names_list, Names_compare):
        """Compare two list,(Names_list, Names_compare) only for find_book() function, if value are not the same

    return error with index position error. if value are same, attribute the required value in variable and return them in a list.

    Name's list is what we want, Names_compare is only the sevens "tr" tag values in the html of one book url."""
  
        info = []

        if Names_list[0] in Names_compare[0].th:
            universal_product_code = Names_compare[0].find("td").text
            info.append(universal_product_code)
            #print("yes", universal_product_code)
        else:
            print("UPC not in compare list[0]")
        if Names_list[1] in Names_compare[2].th:
            price_excluding_tax = Names_compare[2].find("td").text
            #print("yes", price_excluding_tax)
            info.append(price_excluding_tax)
        else:
            print("Price (excl. tax) not in compare list[2]")     
        if Names_list[2] in Names_compare[3].th:
            price_including_tax = Names_compare[3].find("td").text
            #print("yes", price_including_tax)
            info.append(price_including_tax)
        else:
            print("Price (incl. tax) not in compare list[3]")
        if Names_list[3] in Names_compare[5].th:
            Availability = Names_compare[5].find("td").text
            #print("yes", Availability)
            info.append(Availability)
        else:
            print("Availability not in compare list[5]") 

        return info  

def category_index_urls():
    
    """ With the main page url, look for all urls of each category and return them in a list (category_link), with this list,
    test each url to know if the category has multiple pages, at the same time store each category 
    name as key and their corresponding page as list inside in a dictionary (cat_names)  """

    cat_names = {}
    percent = 0
    category_links = all_category_links()

    for link in category_links:
        responsive = requests.get(link)            
        if responsive.ok:
            link = link.replace("index.html", "page-1.html")
            resp = requests.get(link)
            if resp.ok:
                name_cat = link.split("_")[0].replace("http://books.toscrape.com/catalogue/category/books/", "")
                # Create dict with name_cat as list and key.
                cat_names[name_cat] = []
                b = 1
                writing(name_cat) #writing csv with name_cat as name
                percent += 2
                print("Writing of " + name_cat + ".csv"+" (" + str(percent) + "% " + "completed)")
                while resp.ok:
                    # Append link to name_cat list in cat_names dict
                    cat_names[name_cat].append(link)
                    b += 1
                    link = link.replace("page-" + str(b - 1) + ".html", "page-" + str(b) + ".html")
                    resp = requests.get(link)
            else:
                link = link.replace("page-1.html", "index.html")
                name_cat = link.split("_")[0].replace("http://books.toscrape.com/catalogue/category/books/", "")
                writing(name_cat) #writing csv with name_cat as name
                percent += 2
                print("Writing of " + name_cat + ".csv"+" (" + str(percent) + "% " + "completed)")
                cat_names[name_cat] = [link]

    return cat_names[name_cat]            
               
                
"""        
        for link in cat_names[name_cat]:
            
            books_links = search_books_cat(link)
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

                    writer = csv.DictWriter(f, fieldnames=colums_name, delimiter="\t")
                    writer.writerow({                            
                    "[product_page_url]" : book_link,
                    "[upc]" : info[0],
                    "[title]" : info[5],
                    "[price_including_tax]" : info[1],
                    "[price_excluding_tax]" : info[2],
                    "[number_available]" : info[3],
                    "[product_description]" : info[6],
                    "[category]" : info[4],
                    "[review_rating]" : info[8],
                    "[img_url]" : info[7]
                    })
                    """
                                     
def search_books_cat(category_link):

    """ with values as category_link, return all books links of category_link in a list """

    books_links = []
    url = category_link
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.content, "lxml")
        info_book_url = soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        for h3 in info_book_url:                              
            
                a = h3.find("a")
                book_link = a["href"].replace("../../../", "")
                books_links.append("http://books.toscrape.com/catalogue/" + book_link)

    return books_links   
        
def writing(name_csv):
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
  
def all_category_links():


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

def append_to_csv(name_cat):
    
    cat_names = category_index_urls()
    for link in cat_names[name_cat]:
            
            books_links = search_books_cat(link)
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

                    writer = csv.DictWriter(f, fieldnames=colums_name, delimiter="\t")
                    writer.writerow({                            
                    "[product_page_url]" : book_link,
                    "[upc]" : info[0],
                    "[title]" : info[5],
                    "[price_including_tax]" : info[1],
                    "[price_excluding_tax]" : info[2],
                    "[number_available]" : info[3],
                    "[product_description]" : info[6],
                    "[category]" : info[4],
                    "[review_rating]" : info[8],
                    "[img_url]" : info[7]
                    })

category_index_urls()