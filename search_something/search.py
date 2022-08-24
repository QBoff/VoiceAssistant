import requests
from bs4 import BeautifulSoup
import pymorphy2
from num2t4ru import num2text

morph = pymorphy2.MorphAnalyzer()

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 \
                Safari/537.36 Edg/89.0.774.57'
}


def search_weather(text_to_search="какая сейчас погода"):

    req = requests.get(f"https://www.google.com/search?q={text_to_search}",
                       headers=headers)

    soup = BeautifulSoup(req.content, "html.parser")

    try:
        allInfo = soup.find(class_="UQt4rd")
    except AttributeError:
        return "Я не смогла найти погоду."

    degrees = allInfo.find(class_="wob_t q8U8x").get_text()
    otherInfo = allInfo.find(class_="wtsRwe").find_all("div")
    n = int(otherInfo[0].get_text()[-3:-1])
    n2 = int(otherInfo[1].get_text()[-3:-1].strip())
    n3 = int(otherInfo[2].get_text()[-10:-9])

    num1 = morph.parse('процент')[0].make_agree_with_number(n).word
    num2 = morph.parse('метр')[0].make_agree_with_number(n3).word

    result = f"Сейчас на улице {num2text(int(degrees))} градусов. \
        {otherInfo[0].get_text()[:-3]}" +\
        f"{num2text(int(otherInfo[0].get_text()[-3:-1]))} \
            {num1}. " +\
        f"{otherInfo[1].get_text()[:-3]}{num2text(n2)} \
            {morph.parse('процент')[0].make_agree_with_number(n2).word}. " + \
        f"{otherInfo[2].get_text()[:-10]}{num2text(n3)} {num2} в секунду."

    return result

# print(search_weather("какая сейчас погода"))


def search_req(text_to_search: str):
    if "что такое" in text_to_search:
        req = requests.get(f"https://www.google.com/search?q={text_to_search}",
                           headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        try:
            info = soup.find(class_="kno-rdesc").find("span")
            info = info.get_text().split(". ")[0] + "."
        except AttributeError:
            return "Я не смогла найти это в гугле. Простите"

        return info

    elif "когда" in text_to_search or "когда родился" in text_to_search:
        req = requests.get(f"https://www.google.com/search?q={text_to_search}",
                           headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        numbers = ["первого", "второго", "третьего", "четвёртого"]
        try:
            nameOfPerson = soup.find(class_="GzssTd").find("span").get_text()
            info = soup.find(class_="Z0LcW").get_text()  # CfV8xf
            true_num = int(info.split(" ")[0])
            true_year = int(info.split(" ")[2])

            if true_num <= 4:
                true_num = numbers[true_num - 1]
            elif true_num == 7:
                true_num = "седьмого"
            elif 5 <= true_num <= 20:
                true_num = num2text(true_num)[:-1] + "ого"
            elif 21 <= true_num <= 24:
                true_num = num2text(true_num).split(" ")[0] + " " + \
                    numbers[true_num - 21]
            elif 25 <= true_num <= 29:
                true_num = num2text(true_num).split(" ")[0] + " " + \
                    num2text(true_num)[1][:-1] + "ого"
            elif true_num == 30:
                true_num = "тридцатого"
            elif true_num == 31:
                true_num = "тридцать первого"

            if 1 <= int(str(true_year)[-1]) <= 4:
                true_year = " ".join(num2text(true_year).split(" ")[:-1]) + \
                    f" {numbers[int(str(true_year)[-1]) - 1]}"
            elif 5 <= int(str(true_year)[-1]) <= 9:
                true_year = num2text(true_year)[:-1] + " ого"
            # return f"{nameOfPerson} родился {true_num} {info.split(' ')[1]} +
            # {true_year} года."
        except AttributeError:
            return "Я не смогла найти это в гугле. Простите"

        return f"{nameOfPerson} родился {true_num} {info.split(' ')[1]} \
{true_year} гoода."


# print(search_req("когда родился леонардо ди каприо"))
