import asyncio
from telegram import Update, ChatPermissions
from telegram.ext import (
    ApplicationBuilder,
    ChatMemberHandler,
    ContextTypes,
)

BOT_TOKEN = "8237376549:AAHA_xlxX6e4FLqvnwoOi_zgzi10t_mFUFM"

# When new user joins
async def verify_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = update.chat_member
    new_user = member.new_chat_member.user

    # If user just joined
    if member.new_chat_member.status == "member":
        chat_id = update.effective_chat.id
        user_id = new_user.id

        # MUTE USER
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
        )

        # Wait 60 seconds before kicking
        await asyncio.sleep(60)

        # KICK USER
        await context.bot.ban_chat_member(chat_id, user_id)
        await context.bot.unban_chat_member(chat_id, user_id)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(ChatMemberHandler(verify_user, ChatMemberHandler.CHAT_MEMBER))

    app.run_polling()

if __name__ == "__main__":
    main()