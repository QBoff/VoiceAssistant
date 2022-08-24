from bs4 import BeautifulSoup
import requests


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 \
                Safari/537.36 Edg/89.0.774.57'
}
req = requests.get("https://www.maximonline.ru/humor/\
    luchshie-anekdoty-s-chyornym-yumorom-chast-1-id685643/", headers=headers)

soup = BeautifulSoup(req.content, "html.parser")

jokes = soup.find_all(class_="block-text")

with open("jokes/jokes.txt", "w", encoding="utf-8") as file:
    for joke in jokes:
        if joke.find("p") is not None:

            file.write(joke.find("p").text.replace("\xa0", " ") + "\n")

# with open("jokes/jokes.txt", "r", encoding="utf8") as file:
    # print(file.read().split("\n"))
