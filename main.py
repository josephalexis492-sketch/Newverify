import logging
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# PUT YOUR TOKEN & ID HERE
# =========================
BOT_TOKEN = "8237376549:AAHA_xlxX6e4FLqvnwoOi_zgzi10t_mFUFM"
OWNER_ID = 6548935235  # Your Telegram ID

# =========================
# LOGGING
# =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =========================
# MEMORY STORAGE
# =========================
pending_codes = {}
verified_users = set()

# =========================
# COMMANDS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in verified_users:
        await update.message.reply_text("✅ You are already verified!")
        return

    code = str(random.randint(100000, 999999))
    pending_codes[user_id] = code

    await update.message.reply_text(
        f"🔐 Verification Required\n\n"
        f"Send this code back to verify:\n\n"
        f"`{code}`",
        parse_mode="Markdown"
    )

async def verify_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id in verified_users:
        return

    if user_id in pending_codes and text == pending_codes[user_id]:
        verified_users.add(user_id)
        del pending_codes[user_id]
        await update.message.reply_text("✅ Verification successful!")
    else:
        await update.message.reply_text("❌ Wrong code. Try again.")

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verify_input))

    print("Verifier Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()