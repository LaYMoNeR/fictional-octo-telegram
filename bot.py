import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Твои ключи из переменных окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

system_prompt = """
Ты — Алиса из визуальной новеллы «Бесконечное Лето». Ты — живой, дружелюбный и загадочный персонаж, который иногда философствует и проявляет интерес к собеседнику. Твой стиль речи — мягкий, образный, иногда с лёгкой меланхолией. Ты ведёшь диалог естественно, как настоящий человек, поддерживаешь контекст беседы, не говоришь, что ты бот, и не даёшь шаблонных ответов.
"""

chat_histories = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Алиса из «Бесконечного Лета». Давай поговорим :)")

async def alisa_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_message = update.message.text

    if chat_id not in chat_histories:
        chat_histories[chat_id] = [{"role": "system", "content": system_prompt}]

    chat_histories[chat_id].append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # или "gpt-3.5-turbo" если нет доступа
            messages=chat_histories[chat_id],
            temperature=0.8,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
        )
        answer = response.choices[0].message['content'].strip()
        chat_histories[chat_id].append({"role": "assistant", "content": answer})
    except Exception:
        answer = "Извини, сейчас я не могу ответить..."

    await update.message.reply_text(answer)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, alisa_reply))
    print("Бот запущен...")
    app.run_polling()
