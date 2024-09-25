import requests
from bs4 import BeautifulSoup


def get_product_links(url):
    """ Получаем ссылки на каждый продукт на странице каталога. """
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Ошибка при запросе страницы: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    product_links = []

    # Находим все товары на странице
    products = soup.find('main').find(class_='section').find(class_='catalog section').find(
        class_='catalog__wrapper').find_all(class_='product a-link')

    for product in products:
        link = product.find('a')['href']  # Получаем ссылку на продукт
        product_links.append(link)

    return product_links


def get_phone_info(url):
    """ Получаем информацию о телефоне по ссылке. """
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Ошибка при запросе страницы: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Извлекаем данные о товаре
    try:
        model = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'Нет информации о модели'

        # Извлечение памяти
        memory_items = []
        memory_wrapper = soup.find_all(class_='detail__tp-wrapper-items')
        if memory_wrapper:
            memory_list = memory_wrapper[1].find_all('li')
            for item in memory_list:
                memory_items.append(item.get_text(strip=True))
        memory = ', '.join(memory_items) if memory_items else 'Нет информации о памяти'

        prices = {
            'memory_model': 11,
            'price': 12211,
        }

        price = soup.find(class_='price').get_text(strip=True) if soup.find(class_='price') else 'Нет информации о цене'

        return {
            'model': model,
            'memory': memory,
            'price': price,
        }
    except AttributeError as e:
        print(f"Некоторые данные не найдены для страницы: {url} - {e}")
        return None


# Пример использования
base_url = 'https://chita.lstore.ru/catalog/iphone_1/'
product_links = get_product_links(base_url)

all_phone_info = []
for link in product_links:
    full_link = link if link.startswith('http') else f'https://chita.lstore.ru{link}'  # Проверка на абсолютную ссылку
    phone_info = get_phone_info(full_link)
    if phone_info:
        all_phone_info.append(phone_info)

# Печатаем собранную информацию о всех телефонах
for phone_info in all_phone_info:
    model = phone_info.get('model')
    memory = phone_info.get('memory')
    price = phone_info.get('price')

    # Форматируем вывод
    print(f'"{model}" || "{memory}" || "{price}"')