import asyncio
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ChatPermissions,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# =========================
# 🔥 PASTE YOUR TOKEN HERE
# =========================
BOT_TOKEN = "8237376549:AAHA_xlxX6e4FLqvnwoOi_zgzi10t_mFUFM"

VERIFY_TIMEOUT = 60  # seconds
pending_users = {}


# When new member joins
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        user_id = member.id
        chat_id = update.effective_chat.id

        # Mute user
        await context.bot.restrict_chat_member(
            chat_id,
            user_id,
            permissions=ChatPermissions(can_send_messages=False)
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Verify", callback_data=f"verify_{user_id}")]
        ])

        msg = await update.message.reply_text(
            f"👋 Welcome {member.mention_html()}!\n"
            f"Click verify within {VERIFY_TIMEOUT} seconds or you will be kicked.",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

        pending_users[user_id] = {
            "chat_id": chat_id,
            "message_id": msg.message_id
        }

        asyncio.create_task(timeout_kick(context, user_id))


# Kick if not verified
async def timeout_kick(context, user_id):
    await asyncio.sleep(VERIFY_TIMEOUT)

    if user_id in pending_users:
        chat_id = pending_users[user_id]["chat_id"]

        try:
            await context.bot.ban_chat_member(chat_id, user_id)
            await context.bot.unban_chat_member(chat_id, user_id)
        except:
            pass

        del pending_users[user_id]


# Verify button
async def verify_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data != f"verify_{user_id}":
        await query.answer("This is not your button!", show_alert=True)
        return

    if user_id in pending_users:
        chat_id = pending_users[user_id]["chat_id"]

        await context.bot.restrict_chat_member(
            chat_id,
            user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )

        await query.edit_message_text("✅ You are verified!")
        del pending_users[user_id]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Verifier Bot Running")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    app.add_handler(CallbackQueryHandler(verify_button))

    print("🚀 Bot Started")
    app.run_polling()


if __name__ == "__main__":
    main()