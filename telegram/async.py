# Пример синхронного обращения к API

# импорт модулей
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import ContextTypes
from telegram import Update                    
from dotenv import load_dotenv
import os
import requests
import aiohttp

# загружаем переменные окружения
load_dotenv()

# токен бота
TOKEN = os.getenv('TG_TOKEN')

# функция-обработчик команды /start
async def start(update, context):

    # сообщение пользователю
    await update.message.reply_text("Привет! Это пример асинхронного обращения к API")

# функция-обработчик текстовых сообщений
async def text(update, context):
    # Отправляем сообщение "Ожидание ответа..."
    waiting_message = await update.message.reply_text("Ожидание ответа...")

    try:
        # Параметры для обращения к API
        param = {
            'text': update.message.text
        }    
        async with aiohttp.ClientSession() as session:
            async with session.post('http://127.0.0.1:8000/get_answer_async', json=param) as response:
                # Проверяем успешность ответа от API
                if response.status == 200:
                    # Получение ответа от API
                    answer = await response.json()
                    # Обновляем сообщение "Ожидание ответа..." ответом от API
                    await waiting_message.edit_text(answer['message'])
                else:
                    # В случае ошибки API отправляем сообщение об ошибке
                    await waiting_message.edit_text("Произошла ошибка при обращении к API.")
    except Exception as e:
        # Обрабатываем исключения (например, проблемы с сетью)
        await waiting_message.edit_text(f"Произошла ошибка: {e}")

# функция "Запуск бота"
def main():

    # создаем приложение и передаем в него токен
    application = Application.builder().token(TOKEN).build()

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT, text))

    # запускаем бота (нажать Ctrl-C для остановки бота)
    print('Бот запущен...')    
    application.run_polling()
    print('Бот остановлен')

# проверяем режим запуска модуля
if __name__ == "__main__":      # если модуль запущен как основная программа

    # запуск бота
    main()