import os
import sys
import re
import requests
from bs4 import BeautifulSoup
import colorama
from colorama import Fore, Style


class TextBasedBrowser:

    def __init__(self, directory: str):
        self.directory = directory
        self.cache = []

    def cache_page(self, url: str, content: str):
        filename = re.search(r"(\w+\.)+", url).group()[:-1]
        try:
            os.mkdir(self.directory)
        except FileExistsError:
            pass
        os.chdir(self.directory)
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        print("\n file successfully saved")

    def visit_page(self, url: str):
        try:
            r = requests.get(url) if url.startswith("http://") else requests.get("".join(("http://", url)))
        except requests.exceptions.ConnectionError:
            print("Incorrect URL")
        else:
            if r.status_code != 200:
                print("Connection ERROR!")
            else:
                tags = ['p', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
                soup = BeautifulSoup(r.text,
                                     "html.parser").body.descendants  # zooming in on a body part of the "tree" using .body method,
                # + visit all children (descendants) of body tag using .descendants mehtod
                page = ""
                for descendant in soup:
                    if descendant.name in tags:
                        page += Fore.BLUE + descendant.get_text().strip() if descendant.name == "a" else Style.RESET_ALL + descendant.get_text().strip()
                print(page)
                self.cache_page(url, page)
                self.cache.append(page)

    def show_previous_page(self):
        if len(self.cache) > 1:
            self.cache.pop()
            print(self.cache.pop())

    def run_browser(self):
        while True:
            url = input()
            if url == "back":
                self.show_previous_page()
            elif url == "exit":
                break
            else:
                self.visit_page(url)


if __name__ == "__main__":
    colorama.init(autoreset=True)
    browser = TextBasedBrowser(sys.argv[1])  # index 1 as 0 corresponds to the python script file.
    browser.run_browser()
