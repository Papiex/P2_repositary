from main_functions import all_category_links, writing_to_csv, append_to_csv, split_name_category

import requests


cat_names = {}
category_links = all_category_links()

for link in category_links:
    responsive = requests.get(link)

    if responsive.ok:
        link = link.replace("index.html", "page-1.html")
        resp = requests.get(link)

        if resp.ok:
            # Split url for return name category
            name_cat = split_name_category(link)
            # create list (name_cat) in dict (cat_names)
            cat_names[name_cat] = []
            b = 1
            # writing csv with name_cat as name
            writing_to_csv(name_cat)

            while resp.ok:
                # append page link to name_cat list in cat_names dict
                cat_names[name_cat].append(link)
                b += 1
                link = link.replace("page-" + str(b - 1) +
                                    ".html", "page-" + str(b) + ".html")
                resp = requests.get(link)
            # View docstring of append_to_csv()    
            append_to_csv(cat_names, name_cat)

        else:
            link = link.replace("page-1.html", "index.html")
            name_cat = split_name_category(link)
            # writing csv with name_cat as name
            writing_to_csv(name_cat)
            # append index page to [name_cat] list.
            cat_names[name_cat] = [link]
            # View docstring of append_to_csv()
            append_to_csv(cat_names, name_cat)
