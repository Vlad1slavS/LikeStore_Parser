import re
from telethon import TelegramClient

# Замените значения на свои
api_id = '21493397'  # Ваш api_id (число)
api_hash = 'b3237b66bac239e73eca872ca935e8cd'  # Ваш api_hash (строка)
phone = '79145296916'  # номер телефона с международным кодом
target_channel = 'https://t.me/+7uEm3vcRuBRiNWZi'  # Ссылка на канал

# Создаем клиент
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Запускаем клиент
    await client.start()

    # Получаем ID сообщения от пользователя
    message_id = int(input("Введите ID сообщения: "))

    try:
        # Получаем канал по имени
        channel = await client.get_entity(target_channel)

        # Получаем сообщение по ID в канале
        message = await client.get_messages(channel, ids=message_id)

        # Проверяем, найдено ли сообщение
        if message:
            print("Сообщение найдено!")
            print("Текст сообщения:")
            print(message.text)
        else:
            print("Сообщение не найдено в канале.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Запускаем клиент
with client:
    client.loop.run_until_complete(main())