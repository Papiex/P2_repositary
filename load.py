import csv
import os
import time

from extract import download_picture, search_books_links_category, find_info_book


def make_directory_category(name_category: str) -> None:
    """Make directories => csv files/name_cat/jpg files/"""

    try:
        os.makedirs("csv files/" + name_category + "/jpg files/")

    except BaseException:
        print("Error in creation of directories")
        pass


def writing_to_csv(name_category: str) -> None:
    """with name_csv as name, writing a csv in writing mode"""

    print("Writing of " + name_category.upper() + ".CSV and downloading pictures")
    with open("csv files/" + name_category + "/" + name_category + ".csv", "w", encoding="utf-8") as f:

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


def append_to_csv(category_names_dict: dict[str], name_category: str) -> None:
    """
    call the function search_books_links_category() who go search for all links in the dict {category_names_dict} with the key variable (name_category)
    and return a list [book_links] and for all url in, we call the function find_info_book() who return "book info" in a list [info] and write this list in append mode to the
    current key variable (name_category".csv")
    """
    
    number: int = 1
    book_link_count = 0
    t0 = time.time()

    # call the function search_books_links_cat() for each url in  {dict}=>category_names_dict(key)=>[names_category]<=[list]
    # all books links in will be stored in [books_links]
    for link in category_names_dict[name_category]:
        books_links = search_books_links_category(link)

        # Extract info book for each url in [book_links]
        for book_link in books_links:
            info, no_response = find_info_book(book_link)

            if no_response == False:

                download_picture(info[7], name_category, number)
                # print the progress of books/ picture downloaded
                print(str(book_link_count) + " writed/download...", end="\r")

                with open("csv files/" + name_category + "/" + name_category + ".csv", "a", encoding="utf-8") as f:
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
                
            else:
                continue

    t1 = time.time()
    total = timer(t0, t1)
    # When category is complete print the number of book in and pictures and time elapsed
    print("Done ! " + str(book_link_count) + " Books/Pictures Writed/Download, " + total + (" seconds time elapsed !"))
    print("=========================================================")


def timer(t0: float, t1: float) -> str:
    """calculate time elapsed with t1 - t0 and return total"""
    
    total = t1 - t0
    total = round(total, 3)
    total = str(total)
    return total