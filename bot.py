import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Твой Telegram-токен
TOKEN = "8754092410:AAGg_qzEoSpExWxDvNIwZEvPr1CJJdYURVk"

# Ключ Mistral (потом обязательно замени на новый)
MISTRAL_KEY = "vcveCGvkIYK9ck8aAcguzoT57QgbJlsT"

def ask_mistral(user_text):
    """Отправляет запрос в Mistral API и возвращает ответ"""
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": user_text}]
    }
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=30)
        resp.raise_for_status()  # вызовет ошибку, если статус не 200
        result = resp.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка при запросе к Mistral: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ИИ-бот. Задай мне любой вопрос.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = ask_mistral(user_text)
    await update.message.reply_text(reply)

def main():
    print("Создаю приложение...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Запускаю polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
