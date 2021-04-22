from extract import get_all_category_links
from transform import split_name_category
from code_load import make_directory_category, writing_to_csv, append_to_csv

import os

import requests 

def main():
    
    category_names_dict: dict[str, str] = {}
    category_links = get_all_category_links()

    for link in category_links:
        responsive = requests.get(link)

        if responsive.ok:
            link = link.replace("index.html", "page-1.html")
            resp = requests.get(link)

            if resp.ok:
                # Split url for return name category
                name_category = split_name_category(link)
                # create list (name_category) in dict (category_names_dict)
                category_names_dict[name_category] = []
                b = 1
                # make two dir with name_category and jpg files directory in.
                make_directory_category(name_category)
                # writing csv with name_category as name
                writing_to_csv(name_category)

                while resp.ok:
                    # append page link to name_cat list in cat_names dict
                    category_names_dict[name_category].append(link)
                    b += 1
                    link = link.replace("page-" + str(b - 1) +
                                        ".html", "page-" + str(b) + ".html")
                    resp = requests.get(link)
                # View docstring of append_to_csv()    
                append_to_csv(category_names_dict, name_category)
            
            else:
                link = link.replace("page-1.html", "index.html")
                name_category = split_name_category(link)
                # make two dir with name_cat and jpg files directory in.
                make_directory_category(name_category)
                # writing csv with name_cat as name
                writing_to_csv(name_category)
                # append index page to [name_category] list.
                category_names_dict[name_category] = [link]
                # View docstring of append_to_csv()
                append_to_csv(category_names_dict, name_category)

if __name__ == "__main__":

    main()