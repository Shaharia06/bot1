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

for package in required_packages:
    try:
        __import__(package.split("==")[0])
    except ImportError:
        print(f"📦 {package} ইনস্টল করা হচ্ছে...")
        install_package(package)

# ✅ সব ইম্পোর্ট
import re
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# 🔐 বট টোকেন ও একাধিক অ্যাডমিন আইডি
BOT_TOKEN = "7375483284:AAGqPYBkEHfZumXVN_1KT7-HwlTQT-e8FhM"
ADMIN_IDS = [7949308405, 6919881622, 1087968824]  # একাধিক অ্যাডমিন

# 👮‍♂️ অ্যাডমিন চেক
async def is_admin(update: Update):
    return update.effective_user.id in ADMIN_IDS

# 📌 /info কমান্ড
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("<b>⛔ বাপজান বট কি তোমার বাপের😐🤨? এই কমান্ড শুধুমাত্র অ্যাডমিন ব্যবহার করতে পারবে!🫰</b>", parse_mode=ParseMode.HTML)
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("<b>⚠️ কারো মেসেজে reply দিয়ে /info লিখো।</b>", parse_mode=ParseMode.HTML)
        return

    user = update.message.reply_to_message.from_user
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    user_id = user.id
    username = f"@{user.username}" if user.username else "No username"

    photos = await context.bot.get_user_profile_photos(user.id)
    if photos.total_count > 0:
        photo_file = photos.photos[0][-1].file_id
        await update.message.reply_photo(
            photo=photo_file,
            caption=(
                f"<b>👤 Full Name:</b> <b>{full_name}</b>\n"
                f"<b>🆔 User ID:</b> <code>{user_id}</code>\n"
                f"<b>🔗 Username:</b> <b>{username}</b>"
            ),
            parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_text(
            f"<b>👤 Full Name:</b> <b>{full_name}</b>\n"
            f"<b>🆔 User ID:</b> <code>{user_id}</code>\n"
            f"<b>🔗 Username:</b> <b>{username}</b>",
            parse_mode=ParseMode.HTML
        )

# 📝 /report কমান্ড (সবার ইনবক্সে রিপোর্ট পাঠাবে)
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("<b>❌ রিপোর্ট লিখো! যেমনঃ\n/report কেউ বাজে কথা বলছে</b>", parse_mode=ParseMode.HTML)
        return

    report_text = ' '.join(context.args)
    user = update.effective_user
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    username = f"@{user.username}" if user.username else "No username"
    user_id = user.id

    msg = (
        f"📩 নতুন রিপোর্ট এসেছে:\n\n"
        f"👤 Reporter Info:\n"
        f"• Name: {full_name}\n"
        f"• Username: {username}\n"
        f"• Chat ID: <code>{user_id}</code>\n\n"
        f"📝 রিপোর্ট: {report_text}"
    )

    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=msg, parse_mode=ParseMode.HTML)
        except Exception as e:
            print(f"❌ অ্যাডমিন {admin_id} কে রিপোর্ট পাঠাতে সমস্যা: {e}")

    await update.message.reply_text("<b>✅ রিপোর্ট পাঠানো হয়েছে। ধন্যবাদ।</b>", parse_mode=ParseMode.HTML)

# 📜 /rules কমান্ড (শুধুমাত্র অ্যাডমিনের জন্য)
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("<b>⛔ বাপজান বট কি তোমার বাপের😐🤨? এই কমান্ড শুধুমাত্র অ্যাডমিন ব্যবহার করতে পারবে!🫰</b>", parse_mode=ParseMode.HTML)
        return

    rules_text = (
        "<b>📢 গ্রুপের নিয়মাবলী:</b>\n\n"
        "1️⃣<b> অসভ্য ভাষা ব্যবহার করা যাবে না।</b>❌\n"
        "2️⃣<b> ব্যক্তিগত আক্রমণ নিষিদ্ধ।</b>❌\n"
        "3️⃣<b> স্প্যাম বা অবাঞ্ছিত লিঙ্ক শেয়ার করা যাবে না।</b>❌\n"
        "4️⃣<b> সকল সদস্যকে সম্মান করতে হবে।</b>✅\n"
        "5️⃣<b> অ্যাডমিনদের নির্দেশ মেনে চলতে হবে।</b>✅\n\n"
        "<b>ধন্যবাদ সবাইকে শান্তিপূর্ণ ও মজার গ্রুপ পরিবেশ বজায় রাখার জন্য।</b>🫶💐"
    )
    await update.message.reply_text(rules_text, parse_mode=ParseMode.HTML)

# 🆘 /help কমান্ড (সবার জন্য)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "<b>@TEAM_BCCBOT এ BOT গিয়ে যেকারো বিষয়ে গোপনে রিপোর্ট করতে পারেন।</b>\n\n"
        "<b>যেভাবে রিপোর্ট করবেন:</b>\n"
        "\n"
        "<b>উদাহরণঃ</b> <code> /report &lt;আপনার উক্ত অভিযোগটি লিখুন&gt; </code>\n"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

# 🎉 নতুন মেম্বার এলে স্বাগতম
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        name = member.first_name or "বন্ধু"
        await update.message.reply_text(f"<b>🎉 স্বাগতম {name}! গ্রুপে আসার জন্য ধন্যবাদ। মজা করো, নিয়ম মানো 😊💐</b>", parse_mode=ParseMode.HTML)

# 👋 মেম্বার বের হলে বিদায়
async def left(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.left_chat_member
    if user:
        name = user.first_name or "বন্ধু"
        await update.message.reply_text(f"<b>👋 বিদায় {name}! আশা করি আবার দেখা হবে!🫶</b>", parse_mode=ParseMode.HTML)

# ▶️ বট চালু
if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, left))

    print("✅ Bot is running with multi-admin /report, /info, /rules and /help support")
    app.run_polling()
