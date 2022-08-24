import pywhatkit
import pymorphy2


morph = pymorphy2.MorphAnalyzer()

phones = [
    ("Мама", "+79686182267"),
    ("Игорь", "+79972711325"),
    ("Кирилл", "+79266699009"),
    ("Маша", "+79031531536"),
    ("Никита", "+79261966424"),
    ("Юля", "+79629214575"),
    ("Аристократка", "+79683689434"),
    ("Юристка", "+79653715898"),
]


def send_message(mes: str, recipient: tuple) -> None:
    # print(recipient)
    pywhatkit.sendwhatmsg_instantly(phone_no=recipient[1], message=mes)


def who_is_the_recipient(recipient):

    normal_name = morph.parse(recipient)[0].normal_form

    for item in phones:
        if item[0] == normal_name.capitalize():
            return item

    return "Такого контакта у меня нет...."


# name = morph.parse("Аристократке")[0].normal_form
# name2 = morph.parse("Юристке")[0].normal_form
# print(name, name2)
# n = phones[0][1]
# print("+" in n)
# pywhatkit.sendwhatmsg_instantly(phone_no=n, message="Привет")

# send_message("Привет, как твои дела", who_is_the_recipient("мама"))
