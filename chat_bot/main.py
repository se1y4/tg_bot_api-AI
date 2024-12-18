import asyncio
import logging

import g4f
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Добавил логгирование by design
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Обработка запроса пользователя  
async def generate_response(user_message):
    response = await asyncio.to_thread(
        g4f.ChatCompletion.create,
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )
    return response

async def start(update: Update, context):
    await update.message.reply_text(f"Привет! Я бот на базе нейросети. Задай мне вопрос!")

async def help(update: Update, context):
    await update.message.reply_text("Просто задай вопрос :3")

async def handle_message(update: Update, context):
    user_message = update.message.text
    logger.info(f"Пользователь {update.message.from_user.username} (ID: {update.message.from_user.id}) отправил сообщение: {user_message}")
    try:
        response = await generate_response(user_message)
        await update.message.reply_text(response)
    except Exception as WrongResponse:
        logger.error(f"Ошибка при генерации ответа: {WrongResponse}")
        await update.message.reply_text("Произошла ошибка при обработке вашего запроса.")

if __name__ == "__main__":

    #Токен бота 
    TOKEN = "token"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()