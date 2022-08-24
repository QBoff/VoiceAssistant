import requests as r
from bs4 import BeautifulSoup


def get_currency(currency: str = "rouble"):
    req = r.get("https://www.cbr.ru/currency_base/daily/")
    text = req.text

    with open("search_currency\\site.html", "w", encoding="utf-8") as file:
        file.write(text)

    with open("search_currency\\site.html", "r", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    course = soup.find(class_="data").find("tbody").find_all("tr")

    return int(str(course[11].find_all("td")[4].text.split(",")[0]))


# print(get_currency())
