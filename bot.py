import os
import json
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Получаем токен из переменных окружения (безопасно!)
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Настройка логов
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Бот базы скамеров запущен!\n\n"
        "Команды:\n"
        "/search - поиск\n"
        "/add - добавить\n"
        "/help - помощь"
    )

# Команда /search
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите @username для поиска:")
    context.user_data['mode'] = 'search'

# Команда /add
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите: @username причина")
    context.user_data['mode'] = 'add'

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get('mode')
    
    if mode == 'search':
        await update.message.reply_text(f"🔍 Ищу: {text}\n(Здесь будет поиск по базе)")
    elif mode == 'add':
        await update.message.reply_text(f"✅ Добавлено: {text}")
    else:
        await update.message.reply_text("Используйте /search или /add")
    
    context.user_data['mode'] = None

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
