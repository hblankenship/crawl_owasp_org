import requests

page_list = ["https://www.owasp.org/index.php/Main_Page"]
valid_start = ["/index.php/", "https://www.owasp.org/index.php/"]

def is_valid_start(str):
    for start in valid_start:
        if str.startswith(start):
            return True
    
    return False

def is_special_page(href):
    if href.find("File:") > -1:
        return True
    if href.find("Special:") > -1:
        return True
    if href.find(".php?") > -1:
        return True
    if href.find("Template:") > -1:
        return True
    if href.find("User:") > -1:
        return True
    if href.find("Talk:") > -1:
        return True
    if href.find("#") > -1:
        return True
    
    return False

def add_to_pagelist(pages, textofpage):
    if "<a href=" in textofpage:
        ahrefs = textofpage.split("<a href=")
        for href in ahrefs:
            if href.find("\"") > -1 and len(href) > 2:
                href = href[1:href.find("\"", 1)]
            elif href.find("'") > -1 and len(href) > 2:
                href = href[1:href.find("'", 1)]

            if is_valid_start(href) and not is_special_page(href):
                if href.startswith("/"):
                    href = "https://www.owasp.org" + href
                if href not in pages:
                    pages.append(href)
                    print("Adding " + href + "\n")

    return pages

def crawl_site(pages, index):
    start_count = len(pages)
    for page in pages:
        r = requests.get(page)
        if r.status_code == requests.codes.ok:
            pages = add_to_pagelist(pages, r.text)

    if start_count != len(pages):
       return crawl_site(pages, index + 1)

    return pages


def main():
    pages = crawl_site(page_list, 0)
    with open("wiki_pages.txt", "w") as fileh:
        fileh.write("\n".join(str(item)[32:] for item in pages))


main()