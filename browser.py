import os
import sys

import re
import requests
from bs4 import BeautifulSoup

# write your code here


def mkdir(directory, url, text):
    filename = re.search(r"(\w+)\.", url).group()[:-1]

    try:
        os.mkdir(directory)
    except FileExistsError:
        print("FAILURE")
    else:
        os.chdir(directory)
        with open(filename, "w", encoding="UTF-8") as file:
            file.write(text)
        print("SUCCESS")


def main():
    directory = sys.argv[1]  # 1, not 0

    pages_history = []

    while True:
        url = input()
        if url not in {"exit", "back"}:
            r = requests.get(url) if url.startswith("http://") else requests.get("".join(("http://", url)))
            #print(r.status_code)
            if r.status_code != 200:
                print("ERROR!")
                continue
            else:
                soup = BeautifulSoup(r.content, 'html.parser')
                print(soup.prettify())
                #print(r.content)
                mkdir(directory, url, soup.prettify())
                pages_history.append(soup.prettify())
        elif url == "exit":
            break
        elif url == "back":
            if pages_history:
                pages_history.pop()
                print()


if __name__ == "__main__":
    main()
