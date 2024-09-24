import requests
from bs4 import BeautifulSoup


def get_phone_info(url):
    # Отправляем GET-запрос по указанному URL
    response = requests.get(url)

    # Проверяем успешность запроса
    if response.status_code != 200:
        print(f"Ошибка при запросе страницы: {response.status_code}")
        return None

    # Парсим полученный HTML-код
    soup = BeautifulSoup(response.text, 'html.parser')

    products = soup.find('main').find(class_='section').find(class_='catalog section').find(class_='catalog__wrapper').find(class_='catalog__wrapper-elements').find_all(class_='product a-link')
    print(products)

    all_phone_info = []

    # Ищем необходимые данные
    # Здесь предполагается, что модель, память и цена имеют определённые классы или ID,
    # например, 'model', 'memory', 'price'

    for container in products:
        # Ищем необходимые данные для каждого телефона
        try:
            model = container.find(class_='product__info').find('p').get_text(strip=True)
            memory = container.find(class_='memory').get_text(strip=True)
            price = container.find(class_='price').get_text(strip=True)

            all_phone_info.append({
                'model': model,
            })
        except AttributeError:
            print("Некоторые данные не найдены для этого товара.")

    return all_phone_info

    return {
        'model': model,
        'memory': memory,
        'price': price,
    }


# Пример использования
url = 'https://chita.lstore.ru/catalog/iphone_1/'
phone_info = get_phone_info(url)
print(phone_info)