import subprocess
import sys
import random
import html  # <-- ইম্পোর্ট করো ইউজার ইনপুট এস্কেপের জন্য

# লাইব্রেরি ইনস্টলার
def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
    except subprocess.CalledProcessError:
        print(f"❌ {package} ইনস্টল করতে সমস্যা হয়েছে!")

required_packages = [
    "python-telegram-bot==22.1"
]

for package in required_packages:
    try:
        __import__(package.split("==")[0])
    except ImportError:
        print(f"📦 {package} ইনস্টল করা হচ্ছে...")
        install_package(package)

# সব ইম্পোর্ট
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

BOT_TOKEN = "7375483284:AAGqPYBkEHfZumXVN_1KT7-HwlTQT-e8FhM"
ADMIN_IDS = [7949308405, 1087968824]

async def is_admin(update: Update):
    return update.effective_user.id in ADMIN_IDS

# /info কমান্ড
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text(
            "<b>⛔ বাপজান BOT কি তোর বাপের ?🙂😑😐🤨 হুদাই কমান্ড টেপে 😑🙄</b>",
            parse_mode=ParseMode.HTML
        )
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "<b>⚠️ কারো মেসেজে reply দিয়ে /info লিখো।</b>",
            parse_mode=ParseMode.HTML
        )
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

# /report কমান্ড
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "<b>❌ রিপোর্ট লিখো! যেমনঃ\n/report কেউ বাজে কথা বলছে</b>",
            parse_mode=ParseMode.HTML
        )
        return

    report_text = ' '.join(context.args)
    safe_report_text = html.escape(report_text)  # নিরাপদে এস্কেপ করলাম

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
        f"📝 রিপোর্ট: {safe_report_text}"
    )

    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=msg, parse_mode=ParseMode.HTML)
        except Exception as e:
            print(f"❌ অ্যাডমিন {admin_id} কে রিপোর্ট পাঠাতে সমস্যা: {e}")

    await update.message.reply_text(
        "<b>✅ রিপোর্ট পাঠানো হয়েছে। ধন্যবাদ।</b>",
        parse_mode=ParseMode.HTML
    )

# /rules কমান্ড
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text(
            "<b>⛔ বাপজান BOT কি তোর বাপের ?🙂😑😐🤨 হুদাই কমান্ড টেপে 😑🙄</b>",
            parse_mode=ParseMode.HTML
        )
        return

    rules_text = (
        "<b>📢 গ্রুপের নিয়মাবলী:</b>\n\n"
        "1️⃣<b> অসভ্য ভাষা ব্যবহার করা যাবে না।</b>❌\n"
        "2️⃣<b> ব্যক্তিগত আক্রমণ নিষিদ্ধ।</b>❌\n"
        "3️⃣<b> স্প্যাম বা অবাঞ্ছিত লিঙ্ক দেওয়া যাবে না</b>❌\n"
        "4️⃣<b> সকল সদস্যকে সম্মান করতে হবে।</b>✅\n"
        "5️⃣<b> অ্যাডমিনদের নির্দেশ মেনে চলতে হবে।</b>✅\n\n"
        "<b>ধন্যবাদ সবাইকে শান্তিপূর্ণ ও মজার গ্রুপ পরিবেশ বজায় রাখার জন্য।</b>🫶💐"
    )
    await update.message.reply_text(rules_text, parse_mode=ParseMode.HTML)

# /help কমান্ড
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "<b>@TEAM_BCCBOT এ BOT গিয়ে যেকারো বিষয়ে গোপনে রিপোর্ট করতে পারেন।</b>\n\n"
        "<b>যেভাবে রিপোর্ট করবেন:</b>\n"
        "\n"
        "<b>উদাহরণঃ</b>  /report &lt;আপনার উক্ত অভিযোগটি লিখুন&gt; \n"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

# নতুন মেম্বার এলে স্বাগতম
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        name = member.first_name or "বন্ধু"
        await update.message.reply_text(
            f"<b>🎉 স্বাগতম {name}! গ্রুপে আসার জন্য ধন্যবাদ। মজা করো, নিয়ম মানো 😊💐</b>",
            parse_mode=ParseMode.HTML
        )

# মেম্বার বের হলে বিদায়
async def left(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.left_chat_member
    if user:
        name = user.first_name or "বন্ধু"
        await update.message.reply_text(
            f"<b>👋 বিদায় {name}! আশা করি আবার দেখা হবে!🫶</b>",
            parse_mode=ParseMode.HTML
        )

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "<b>🤖 BCC GROUP BOT - কমান্ড লিস্ট:</b>\n\n"
        "<b>👑 Admin Only Commands:</b>\n\n"
        "🔎 /info - ইউজারের ইনফো \n"
        "📜 /rules - গ্রুপ নিয়মাবলী\n\n"
        
        "<b>👥 Member Commands:</b>\n\n"
        "🆘 /help - রিপোর্ট করার নিয়ম \n"
        "🚨 /report &lt;অভিযোগ&gt; - কারো বিরুদ্ধে রিপোর্ট \n\n"
        "<b>🛡️ বট ব্যবহারে কোনো সমস্যা হলে রিপোর্ট দিন!</b>"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

# /news কমান্ড
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text(
            "<b>⛔ বাপজান BOT কি তোর বাপের ?🙂😑😐🤨 হুদাই কমান্ড টেপে 😑🙄</b>",
            parse_mode=ParseMode.HTML
        )
        return

    if not context.args or not context.args[0].startswith("@"):
        await update.message.reply_text(
            "<b>⚠️ একটি username দিন! যেমনঃ /news @someone</b>",
            parse_mode=ParseMode.HTML
        )
        return

    target_username = context.args[0]

    roasts = [
        f"{target_username} এত ছ্যাকা খাইছে যে এখন চোখের জল দিয়ে চা বানায়। 😭☕",
        f"{target_username} এর এক্স এখন অন্য কারো 'বেবি' হয়ে গেছে। 🍼",
        f"{target_username} crush কে I love you বলেছিলো, crush বলল – ভাই কি বললেন! 😅",
        f"{target_username} এর প্রেমে পড়লেই নাকি break-up গ্যারান্টি! 📉💔",
        f"{target_username} এতবার ছ্যাকা খাইছে যে এখন তার নাম ছ্যাকা সেন। 😵‍💫",
        f"{target_username} এর বিয়ে হবে – শুধু তার স্বপ্নে। 😪",
        f"{target_username} এখনো এক্স-এর old chat পড়ে রাতে কান্না করে। 😓📱",
        f"{target_username} প্রেম শুরু করলেই universe বলে – আবার শুরু! 😑",
        f"{target_username} এক্স ছেড়ে গেছে, এখন only memories আছে আর Netflix। 🎞️🍿",
        f"{target_username} এর crush ওকে দেখলে নিজের চোখ বন্ধ করে! 🙈",
        f"{target_username} এর বিয়ে হবে এমন গুজব নিয়ে whole গ্রাম হাসে। 🤣",
        f"{target_username} নিজের বিয়েতে guest হবে না, কারণ কেউ নাই! 🤷‍♂️",
        f"{target_username} এত কষ্টে আছে, sad song আর তার বন্ধু হয়ে গেছে। 🎶😭",
        f"{target_username} প্রপোজ করেছিলো, রিজেক্টেড হয়ে এখন কবি হয়ে গেছে। 🖊️",
        f"{target_username} এত lonely যে mirror এর সাথেই কথা বলে। 🪞😢",
        f"{target_username} ex-এর profile পিক দেখে শুধু sigh করে। 😮‍💨",
        f"{target_username} crush-এর স্টোরি দেখেই দিন শুরু করে, আর রাতে হাহাকার! 🌒",
        f"{target_username} এর love story শুরু হতেই breakup হয়ে যায়। 🚫❤️",
        f"{target_username} এর এত এক্স ছিলো যে ফোনের storage শেষ হয়ে গেছে! 😂",
        f"{target_username} এর এক্স এখন তার বোনের বান্ধবীর বান্ধবীর বয়ফ্রেন্ড। 🥴",
        f"{target_username} সবসময় বলতো – 'তুমি ছাড়া বাঁচবো না'... এখনো বেঁচে আছে। 🤐",
        f"{target_username} এত ছ্যাকা খায় যে তার হৃদয় এখন ভাইরাসে ভরা। 💔🦠",
        f"{target_username} crush-এর reply পায় না, এখন status দেয় – 'Stay Single, Stay Strong' 💪",
        f"{target_username} ex কে নিয়ে poetry লেখে, অথচ কেউ পড়ে না! 📖😆",
        f"{target_username} এর বিয়ের খোঁজ পত্রিকা ছাড়া আর কোথাও নেই। 📰",
        f"{target_username} বিয়ে করতে চায়, কিন্তু কনে বলে – আমি ভগবানের জন্য অপেক্ষা করছি। 🙏",
        f"{target_username} কে বিয়ে করলে বুঝবে – জীবন মানে যন্ত্রণা। 😈",
        f"{target_username} এর প্রেমে fall করেছিলো gravity, তাই এত heavy breakup! 🍂",
        f"{target_username} crush কে দেখলেই দোয়া পড়ে – 'হে আল্লাহ, মনকে শক্ত করো!' 🤲",
        f"{target_username} এর এক্স এখন motivational speaker – 'Breakup এ জীবন থেমে থাকে না' 😌",
    ]

    roast_message = random.choice(roasts)

    try:
        await update.message.delete()
    except Exception as e:
        print(f"❌ মেসেজ ডিলিট করতে পারিনি: {e}")

    await update.message.chat.send_message(roast_message, parse_mode=ParseMode.HTML)

# বট চালু
if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, left))
    app.add_handler(CommandHandler("start", start))

    print("✅ Bot is running with multi-admin /report, /info, /rules, /help, and /news support")
    app.run_polling()
