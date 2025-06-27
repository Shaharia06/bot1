import subprocess
import sys

# 🔧 লাইব্রেরি ইনস্টলার
def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
    except subprocess.CalledProcessError:
        print(f"❌ {package} ইনস্টল করতে সমস্যা হয়েছে!")

# 📦 দরকারি প্যাকেজ
required_packages = [
    "python-telegram-bot==22.1"
]

# 🔁 প্যাকেজ ইনস্টলেশন চেক
for package in required_packages:
    try:
        __import__(package.split("==")[0])
    except ImportError:
        print(f"📦 {package} ইনস্টল করা হচ্ছে...")
        install_package(package)

# ✅ সব ইম্পোর্ট
import re
from telegram import Update, ChatMemberUpdated
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ChatMemberHandler
)

# 🔐 বট টোকেন ও অ্যাডমিন আইডি
BOT_TOKEN = "7375483284:AAETWnzTxMzrAoPLUySLzcy0EcMim1l4VI0"
ADMIN_ID = 7949308405

# 🔠 Markdown Escape
def escape_markdown(text: str) -> str:
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{c}' if c in escape_chars else c for c in text)

# 👮‍♂️ অ্যাডমিন চেক
async def is_admin(update: Update):
    return update.effective_user.id == ADMIN_ID

# 📌 /info কমান্ড
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
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        await update.message.reply_text(
            f"👤 *Full Name:* {escape_markdown(full_name)}\n"
            f"🆔 *User ID:* `{user_id}`\n"
            f"🔗 *Username:* {username}",
            parse_mode=ParseMode.MARKDOWN_V2
        )

# 📝 /report কমান্ড
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ রিপোর্টের টেক্সট লিখো, যেমন:\nউদাহরণঃ /report <তোমার রিপোর্ট>"
        )
        return

    report_text = ' '.join(context.args)
    user = update.effective_user
    msg = (
        f"📩 নতুন রিপোর্ট এসেছে:\n\n"
        f"👤 Reporter: {user.mention_html()}\n"
        f"📝 রিপোর্ট: {report_text}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode=ParseMode.HTML)
    await update.message.reply_text("✅ রিপোর্ট পাঠানো হয়েছে। ধন্যবাদ।")

# 🎉 নতুন মেম্বার এলে স্বাগতম
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        name = member.first_name or "বন্ধু"
        await update.message.reply_text(
            f"🎉 স্বাগতম {name}! গ্রুপে আসার জন্য ধন্যবাদ। এখানে সবাই বন্ধু, মজা করো গ্রুপ রুলস মেনে চলো! 😊"
        )

# 👋 মেম্বার বের হলে বিদায়
async def left(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.left_chat_member
    if user:
        name = user.first_name or "বন্ধু"
        await update.message.reply_text(
            f"👋 বিদায় {name}! আশা করি আবার আসবে।"
        )

# 🏁 বট চালু
if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    # ✅ কমান্ড হ্যান্ডলার
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("report", report))

    # 👥 মেম্বার এন্ট্রি ও এক্সিট
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, left))

    print("✅ Bot is running... /info (admin only), /report, Welcome and Left message active")
    app.run_polling()
