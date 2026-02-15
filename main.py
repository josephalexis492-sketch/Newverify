import asyncio
from telegram import Update, ChatPermissions
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ChatMemberHandler,
)

BOT_TOKEN = "8237376549:AAHA_xlxX6e4FLqvnwoOi_zgzi10t_mFUFM"

verification_timeout = 60
pending_users = {}


async def restrict_user(context: ContextTypes.DEFAULT_TYPE, chat_id, user_id):
    await context.bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=ChatPermissions(can_send_messages=False),
    )


async def unrestrict_user(context: ContextTypes.DEFAULT_TYPE, chat_id, user_id):
    await context.bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        ),
    )


async def kick_user(context: ContextTypes.DEFAULT_TYPE, chat_id, user_id):
    await context.bot.ban_chat_member(chat_id, user_id)
    await context.bot.unban_chat_member(chat_id, user_id)


async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        chat_id = update.effective_chat.id
        user_id = member.id

        await restrict_user(context, chat_id, user_id)

        pending_users[user_id] = chat_id

        await update.message.reply_text(
            f"{member.first_name}, verify in 60 seconds using /verify or you will be kicked."
        )

        await asyncio.sleep(verification_timeout)

        if user_id in pending_users:
            await kick_user(context, chat_id, user_id)
            del pending_users[user_id]


async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in pending_users:
        chat_id = pending_users[user_id]
        await unrestrict_user(context, chat_id, user_id)
        del pending_users[user_id]
        await update.message.reply_text("You are verified!")
    else:
        await update.message.reply_text("You are already verified.")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(ChatMemberHandler(new_member, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(CommandHandler("verify", verify))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()