import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# 🔑 Gemini API kaliti
GEMINI_API_KEY = "AIzaSyC7DW5cIQP052cRLu0DZy8fT3JG3h6o2X8"
genai.configure(api_key=GEMINI_API_KEY)

# 🤖 Telegram bot token
TELEGRAM_TOKEN = "8225342146:AAGxbQmJsVSm8T9yQM1_rLR_qz0kDYT7YPQ"

# 👑 Admin ID
ADMIN_ID = 7776798862   # Sizning ID’ingiz

# Gemini modelini chaqirish
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
        # ✅ Foydalanuvchi yozgan xabarni admin’ga yuboramiz
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"👤 Yangi xabar:\n"
                 f"ID: {user_id}\n"
                 f"Username: @{username}\n"
                 f"Xabar: {user_message}"
        )

        # ✅ Gemini javobi
        response = model.generate_content(user_message)
        text = response.text or ""

        # Gemini yuborgan **qalin** belgilarini *qalin* ga almashtiramiz
        text = text.replace("**", "*")

        # MarkdownV2 ga moslash
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
