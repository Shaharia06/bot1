import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

try:
    import telegram
    import telegram.ext
except ImportError:
    print("📦 python-telegram-bot লাইব্রেরি পাওয়া যায়নি, ইনস্টল করা হচ্ছে...")
    install_package("python-telegram-bot")

import re
from telegram import Update, ChatMember, ChatMemberUpdated
from telegram.ext import Application, CommandHandler, ContextTypes, ChatMemberHandler, MessageHandler

BOT_TOKEN = "7375483284:AAETWnzTxMzrAoPLUySLzcy0EcMim1l4VI0"
ADMIN_ID = 7949308405  # শুধু এই আইডির ইউজার /info ব্যবহার করতে পারবে, /report পাবলিক

def escape_markdown(text: str) -> str:
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{c}' if c in escape_chars else c for c in text)

async def is_admin(update: Update):
    return update.effective_user.id == ADMIN_ID

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("⛔ বাপজান BOT কি তোমার বাপের 🙂 ? এই কমান্ড শুধুমাত্র অ্যাডমিন ব্যবহার করতে পারবে!")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ কারো মেসেজে reply দিয়ে `/info` লিখো।")
        return 

    user = update.message.reply_to_message.from_user
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    user_id = user.id
    username = f"@{escape_markdown(user.username)}" if user.username else "No username"

    photos = await context.bot.get_user_profile_photos(user.id)
    if photos.total_count > 0:
        photo_file = photos.photos[0][-1].file_id
        await update.message.reply_photo(
            photo=photo_file,
            caption=(
                f"👤 *Full Name:* {escape_markdown(full_name)}\n"
                f"🆔 *User ID:* `{user_id}`\n"
                f"🔗 *Username:* {username}"
            ),
            parse_mode="MarkdownV2"
        )
    else:
        await update.message.reply_text(
            f"👤 *Full Name:* {escape_markdown(full_name)}\n"
            f"🆔 *User ID:* `{user_id}`\n"
            f"🔗 *Username:* {username}",
            parse_mode="MarkdownV2"
        )

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ রিপোর্টের টেক্সট লিখো, যেমন:\nউদাহরনঃ /report <your report text here>"
        )
        return

    report_text = ' '.join(context.args)
    user = update.effective_user
    msg = (
        f"📩 নতুন রিপোর্ট এসেছে:\n\n"
        f"👤 Reporter: {user.mention_html()}\n"
        f"📝 রিপোর্ট: {report_text}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode="HTML")
    await update.message.reply_text("✅ রিপোর্ট পাঠানো হয়েছে। ধন্যবাদ।")

# --- নতুন অংশ শুরু ---

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # নতুন মেম্বার যোগ দিলে স্বাগতম বার্তা পাঠাবে
    for member in update.message.new_chat_members:
        name = member.first_name or "বন্ধু"
        await update.message.reply_text(
            f"🎉 স্বাগতম {name}! গ্রুপে আসার জন্য ধন্যবাদ। এখানে সবাই বন্ধু, মজা করো গ্রুপ রুলস মেনে চোলো! 😊"
        )

async def left(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # কেউ গ্রুপ ছেড়ে গেলে বিদায় বার্তা পাঠাবে
    user = update.message.left_chat_member
    if user:
        name = user.first_name or "বন্ধু"
        await update.message.reply_text(
            f"👋 বিদায় {name}! আশা করি আবার আসবে।"
        )

# Alternatively, using ChatMemberHandler for member updates:
# async def member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     result = update.chat_member
#     status = result.new_chat_member.status
#     user = result.new_chat_member.user
#     if status == ChatMember.MEMBER:
#         await update.effective_chat.send_message(f"🎉 স্বাগতম {user.first_name}!")
#     elif status == ChatMember.LEFT:
#         await update.effective_chat.send_message(f"👋 বিদায় {user.first_name}!")

# --- নতুন অংশ শেষ ---


if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    # কমান্ড হ্যান্ডলার
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("report", report))

    # নতুন মেম্বার আসলে welcome, মেম্বার গেলে left হ্যান্ডলার
    app.add_handler(MessageHandler(filters=telegram.ext.filters.StatusUpdate.NEW_CHAT_MEMBERS, callback=welcome))
    app.add_handler(MessageHandler(filters=telegram.ext.filters.StatusUpdate.LEFT_CHAT_MEMBER, callback=left))

    print("✅ Bot is running... /info (admin only), /report, Welcome and Left message active")
    app.run_polling()
