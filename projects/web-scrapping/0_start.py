from urllib.request import urlopen
from urllib.error import HTTPError

from bs4 import BeautifulSoup


def get_title(url: str):
    """
    Получение заголовка первого уровня.
    :param url: Ссылка на сайт
    """
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(f"Error: {e}, status code: {e.code}")
        return None

    try:
        soup = BeautifulSoup(html.read(), "html.parser")
        title = soup.body.h1
    except AttributeError as e:
        print(f"Error: {e}")
        return None

    return title


def get_characters_names_by_tag(url: str, tag: str, **attrs):
    """
    Возвращает список всех персонажей из книги по тегу
    :param url: Ссылка на сайт
    :param tag: Тег
    :param attrs: Словарь с атрибутами
    :return: None или список имён
    """
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(f"Error: {e}, status code: {e.code}")
        return None

    try:
        soup = BeautifulSoup(html.read(), "html.parser")
        names = soup.find_all(tag, **attrs)
    except AttributeError as e:
        print(f"Error: {e}")
        return None
    return names


if __name__ == "__main__":
    title = get_title("http://www.pythonscraping.com/pages/page1.html")
    char_names = get_characters_names_by_tag(
        "http://www.pythonscraping.com/pages/warandpeace.html",
        "span",
        **{"class": "green"}
    )

    if title is None:
        print("Title could not be found")
    else:
        print(title)

    if char_names is None:
        print("Character names could not be found")
    else:
        for name in char_names:
            print(name.get_text())
