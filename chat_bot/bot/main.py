import asyncio
import datetime
import logging
import os
import g4f
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config.database import async_session_maker
from models import LogModel

# Добавил логгирование by design
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Обработка запроса пользователя
async def generate_response(user_message):
    response = await asyncio.to_thread(
        g4f.ChatCompletion.create,
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": user_message}],
    )
    return response


async def start(update: Update, context):
    await update.message.reply_text(
        "Привет! Я бот на базе нейросети. Задай мне вопрос!"
    )


async def help(update: Update, context):
    await update.message.reply_text("Просто задай вопрос :3")


async def handle_message(update: Update, context, session=None):
    
    user_message = update.message.text
    try:
        await update.message.reply_text("Формирую ответ...")
        response = await generate_response(user_message)
        await update.message.reply_text(response)
        log = LogModel(
            created_at=datetime.datetime.now(),
            user_request=user_message,
            bot_response=response,
        )
        if session is None:
            async with async_session_maker() as session:
                session.add(log)
                await session.commit()
        logger.info(
            f"Сохранено в базу данных: {log.id} - {log.created_at} - {log.user_request} - {log.bot_response}"
        )

    except Exception as WrongResponse:
        logger.error(f"Ошибка при генерации ответа: {WrongResponse}")
        await update.message.reply_text(
            "Произошла ошибка при обработке вашего запроса."
        )


if __name__ == "__main__":
    # Токен бота
    TOKEN = os.getenv("TOKEN", "")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
