import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# 🔑 Environment Variables’dan olish
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7776798862"))  # Default qiymat

# Gemini konfiguratsiyasi
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def escape_markdown(text: str) -> str:
    """MarkdownV2 formatida ishlamaydigan belgilarni qochiramiz"""
    escape_chars = ['_', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for ch in escape_chars:
        text = text.replace(ch, f"\\{ch}")
    return text

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Noma'lum foydalanuvchi"

    try:
        # Foydalanuvchi xabarini admin’ga yuborish
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"👤 Yangi xabar:\n"
                 f"ID: {user_id}\n"
                 f"Username: @{username}\n"
                 f"Xabar: {user_message}"
        )

        # Gemini javobi
        response = model.generate_content(user_message)
        text = response.text or ""
        text = text.replace("**", "*")  # Qalin belgilarni almashtirish
        text = escape_markdown(text)

        await update.message.reply_text(text, parse_mode="MarkdownV2")

    except Exception as e:
        await update.message.reply_text(f"Xatolik yuz berdi: {e}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    print("✅ Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()

