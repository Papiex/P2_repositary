



def split_name_category(link: str) -> str:
    """Split on underscore for return name category and transform like this historical-fiction => Historical Fiction"""

    link = link.split("_")[0]
    link = link.replace(
        "http://books.toscrape.com/catalogue/category/books/", "")
    link = link.capitalize().replace("-"," ").title()
    return link