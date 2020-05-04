import os
import sys
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore
init(autoreset=True)


# write your code here
dir_name = sys.argv[1]
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

saved_pages = []
prefix = 'https://'

while True:
    url = input()
    file_name = url.lstrip(prefix).replace('/', '_').replace('.', '-')
    if url == 'back':
        if len(saved_pages) > 1:
            with open(f'{dir_name}/{saved_pages.pop(-2)}', 'r') as file:
                print(file.read())
    elif '.' in url:
        if not url.startswith(prefix):
            url = prefix + url
        response = requests.get(url)
        if response:
            page = BeautifulSoup(response.text, 'html.parser')
            with open(f'{dir_name}/{file_name}', 'w', encoding=response.encoding
                      ) as file:
                for element in page.select("body p, a, h1, h2, h3, h4, h5, h6"):
                    if element.name == 'a':
                        print(Fore.BLUE + element.text.strip())
                    else:
                        print(element.text.strip())
                    file.write(element.text)
            saved_pages.append(file_name)
        else:
            print('Error: failed to retrieve URL')
    elif file_name in saved_pages:
        with open(f'{dir_name}/{file_name}', 'r') as file:
            print(file.read())
    elif url == 'exit':
        break
    else:
        print('Error: Incorrect URL')
        continue
