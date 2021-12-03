import os
import sys

import re
import requests

# write your code here


def mkdir(directory, url, text):
    filename = re.search(r"(\w+\.)+", url).group()[:-1]
    try:
        os.mkdir(directory)
    except FileExistsError:
        pass
    os.chdir(directory)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    print("\n file successfully saved")


def main():
    directory = sys.argv[1]  # 1, not 0

    pages_history = []

    while True:
        url = input()
        if url not in {"exit", "back"}:
            r = requests.get(url) if url.startswith("http://") else requests.get("".join(("http://", url)))
            if r.status_code != 200:
                print("ERROR!")
                continue
            else:
                print(r.text)
                mkdir(directory, url, r.text)
                pages_history.append(r.text)
        elif url == "exit":
            break
        elif url == "back":
            if pages_history:
                pages_history.pop()
                print()


if __name__ == "__main__":
    main()
