import re
from telethon import TelegramClient
from telethon.errors import ChannelPrivateError, ChatIdEmptyError
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Замените значения на свои
api_id = '21493397'  # Ваш api_id (число)
api_hash = 'b3237b66bac239e73eca872ca935e8cd'  # Ваш api_hash (строка)
phone = '79145296916'  # номер телефона с международным кодом
target_channel = 'https://t.me/+7uEm3vcRuBRiNWZi'  # Ссылка на канал
target_message_id = [17, 1495, 1496]  # ID сообщения, которое вы хотите получить
# Авторизация в Google Таблицах
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('secret-key.json', scope)
gc = gspread.authorize(credentials)

# Открываем таблицу
spreadsheet_name = 'tovary'
spreadsheet = gc.open(spreadsheet_name)
worksheet = spreadsheet.worksheet('Лист1')

# Создаем клиент
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Запускаем клиент
    await client.start()

    try:
        # Получаем канал
        channel = await client.get_entity(target_channel)
        row = 2
        # Получаем сообщение по ID

        for i in range (len(target_message_id)):
            message = await client.get_messages(channel, ids=target_message_id[i])

            # Извлечение названий товаров с флагами и ценами с помощью регулярного выражения

            items = re.findall(r'([🇺🇸🇬🇧🇨🇦🇩🇪🇫🇷🇯🇵🇮🇳🇦🇪🇨🇳]*[^\n–]+) – (\d{1,3}(?:\.\d{3})*(?:,\d{1,2})?₽)', message.text)
            print(items)

            # Выводим найденные названия и цены
            if items:
                print("Найденные товары с ценами:")
                for i, (country_flag, price) in enumerate(items):
                    # Удаляем лишние пробелы
                    country_flag = country_flag.strip()
                    words = country_flag.split()
                    color = ' '.join(words[-2])
                    model_name = ' '.join(words[:-2])  # Название модели - все слова кроме последнего
                    last_word = words[-1]  # Последнее слово - флаг или другая информация
                    worksheet.update_cell(row, 1, model_name)
                    worksheet.update_cell(row, 2, color)
                    worksheet.update_cell(row, 3, last_word)
                    worksheet.update_cell(row, 4, price)
                    row += 1
                    print(i)
                    time.sleep(3)
            else:
                print("Товары не найдены.")

        else:
            print("Сообщение не найдено.")

    except ChannelPrivateError:
        print("Канал закрытый. Убедитесь, что вы участник канала.")
    except ChatIdEmptyError:
        print("Не удалось получить ID чата.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Запускаем клиент
with client:
    client.loop.run_until_complete(main())