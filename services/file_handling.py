BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


# Функція, яка повертає строку з текстом сторінки і її розміром
def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    temp: str = text[start:int(start + page_size)]

    punctuation_mark: str = '.,!:;?'

    if temp[-1] in punctuation_mark and temp[-2] in punctuation_mark and temp[-3] in punctuation_mark:
        temp: str = temp[0:-3]
    elif temp[-1] in punctuation_mark and temp[-2] in punctuation_mark and temp[-3].isalpha():
        temp: str = temp[0:-2]

    while temp[-1] not in punctuation_mark:
        temp: str = temp[0: -1]

    return temp, len(temp)


# Функція, яка форматує словарь книги
def prepare_book(path: str) -> None:
    num_key: int = 1
    with open(path, 'r', encoding='utf-8') as text:
        text = text.read()
    while len(text) != 0:
        tuple_value_size: tuple[str, int] = _get_part_text(text, 0, 1050)
        book[num_key]: str = tuple_value_size[0].lstrip()
        num_key += 1
        text: str = text[tuple_value_size[1] + 1:]


# Визов функції prepare_book для підготовки книги із текстового файла
prepare_book(BOOK_PATH)
