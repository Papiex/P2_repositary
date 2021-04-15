from extracting_functions import search_books_links_cat, picture_download
from transformation_functions import find_info_book

import csv
import os






#code_loading
def make_dir_category(name_cat):
    """Make directories => csv files/name_cat/jpg files/"""

    try:
        os.makedirs("csv files/" + name_cat + "/jpg files/")

    except:
        print("Error in creation of directories")
        pass

#code_loading
def writing_to_csv(name_cat):
    """with name_csv as name, writing a csv in writing mode"""
    
    print("Writing of " + name_cat + ".csv and downloading pictures")
    with open("csv files/" + name_cat + "/" + name_cat + ".csv", "w", encoding="utf-8") as f:

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
            "[img_url]",
            "[img_name]"
        ]

        writer = csv.DictWriter(f, fieldnames=colums_name, delimiter="\t")
        writer.writeheader()

#code_loading
def append_to_csv(cat_names, name_cat):
    """call the function search_books_links_cat() who go search for all links in the dict {cat_names} with the key variable (name_cat)
    and return a list [book_links] and for all url in, we call the function find_info_book() who return "book info" in a list [info] and write this list in append mode to the
    current key variable (name_cat".csv") """
    
    # transform variable number in to global variable 
    # and for each function call, reset value of number to "1"
    global number
    number = 1
    book_link_count = 0
    # call the function search_books_links_cat() for each url in  {dict}=>cat_names(key)=>[names_cat]<=[list]
    # all books links in will be stored in [books_links]
    for link in cat_names[name_cat]:      
        books_links = search_books_links_cat(link)
        # Extract info book for each url in [book_links] 
        for book_link in books_links:
            info = find_info_book(book_link)
            picture_download(info[7], name_cat, number)
            # print the progress of books/ picture downloaded
            print(str(book_link_count) + " writed, " + str(number-1) + " downloaded", end="\r")
            
            with open("csv files/" + name_cat + "/" + name_cat + ".csv", "a", encoding="utf-8") as f:

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
                    "[img_url]",
                    "[img_name]"
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
                    "[img_url]": info[7],
                    "[img_name]": ("Picture_" + str(number) + ".jpg")
                })
            number += 1
            book_link_count += 1
    # When category is complete print the number of book in and pictures        
    print("Done ! " + str(book_link_count) + " books info writed, " + str(number-1) + " pictures downloaded")  