import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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


def get_memory_infos(url):
    """Получаем информацию о размерах памяти и ценах для каждой модели."""

    # Создаем экземпляр веб-драйвера
    driver = webdriver.Chrome()  # Убедитесь, что ChromeDriver в вашем PATH

    driver.get(url)

    # Создаем словарь для хранения информации
    memory_infos = {}

    try:
        # Находим заголовок модели
        model = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        ).text

        # Находим все кнопки с размерами памяти
        memory_buttons = driver.find_elements(By.CLASS_NAME, 'detail__tp-item')  # Замените на правильный класс

        for button in memory_buttons:
            # Имитируем клик по кнопке
            button.click()
            time.sleep(1)  # Ожидание загрузки контента

            # Собираем размер памяти
            memory_size = button.text()

            # Получаем цену из элемента с классом 'detail__price-current'
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'detail__price-current'))
            )
            price = price_element.text if price_element else 'Нет информации о цене'

            # Сохраняем информацию в словарь
            memory_infos[memory_size] = price

            # Если хотите вернуться назад после получения информации
            driver.back()  # Возвращаемся на предыдущую страницу
            time.sleep(1)  # Ожидание после возврата

            # Обновляем кнопки памяти после возврата
            memory_buttons = driver.find_elements(By.CLASS_NAME, 'detail__tp-item')

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()  # Закрываем браузер после завершения

    return {
        'model': model,
        'memory_infos': memory_infos,
    }


# Пример использования
base_url = 'https://chita.lstore.ru/catalog/iphone_1/'  # Замените на нужную ссылку
product_links = ['https://chita.lstore.ru/catalog/iphone_1/iphone_16/','https://chita.lstore.ru/catalog/iphone_1/iphone_16_pro/']

all_phone_info = []

for link in product_links:
    # full_link = link if link.startswith('http') else f'https://chita.lstore.ru{link}'  # Проверка на абсолютную ссылку
    phone_info = get_memory_infos(link)
    if phone_info:
        all_phone_info.append(phone_info)

print(all_phone_info)  # Печатаем собранную информацию о модели
