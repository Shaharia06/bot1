import subprocess
import sys

# যদি module না থাকে, তাহলে অটো ইনস্টল করবে
try:
    from telegram import Update, ChatMemberUpdated
    from telegram.ext import (
        Application, CommandHandler, ContextTypes,
        ChatMemberHandler
    )
except ImportError:
    print("📦 python-telegram-bot পাওয়া যায়নি, ইনস্টল করা হচ্ছে...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "python-telegram-bot"])
    from telegram import Update, ChatMemberUpdated
    from telegram.ext import (
        Application, CommandHandler, ContextTypes,
        ChatMemberHandler
    )

import re

BOT_TOKEN = "8135386559:AAGKbt0LjPupSmYQQ-f5_FM2JzakFuxNkAM"
ADMIN_ID = 6919881622  # শুধু এই আইডি info চালাতে পারবে

def escape_markdown(text: str) -> str:
    escape_chars = r'\_*[]()~>#+-=|{}.!'
    return ''.join(f'\\{c}' if c in escape_chars else c for c in text)

async def is_admin(update: Update):
    return update.effective_user.id == ADMIN_ID

# ✅ /info command
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("⛔ বাপজান BOT কি তোমার বাপের 🙂 ? এই কমান্ড শুধুমাত্র অ্যাডমিন ব্যবহার করতে পারবে!")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ কারো মেসেজে reply দিয়ে /info লিখো।")
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
                f"🆔 *User ID:* {user_id}\n"
                f"🔗 *Username:* {username}"
            ),
            parse_mode="MarkdownV2"
        )
    else:
        await update.message.reply_text(
            f"👤 *Full Name:* {escape_markdown(full_name)}\n"
            f"🆔 *User ID:* {user_id}\n"
            f"🔗 *Username:* {username}",
            parse_mode="MarkdownV2"
        )

# ✅ /report command
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ রিপোর্টের টেক্সট লিখো, যেমন:\nউদাহরণঃ /report <তোমার রিপোর্ট>")
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

# ✅ নতুন মেম্বার এলে স্বাগতম
async def welcome_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = update.chat_member.new_chat_member
    if member.status == "member":
        user = member.user
        full_name = user.full_name
        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text=f"🌟 স্বাগতম {full_name}!\nআশা করি তুমি ভালো সময় কাটাবে আমাদের সাথে ❤️"
        )

# ✅ কেউ লিভ করলে বিদায়
async def farewell_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = update.chat_member
    if member.old_chat_member.status == "member" and member.new_chat_member.status in ("left", "kicked"):
        user = member.new_chat_member.user
        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text=f"👋 বিদায় {user.full_name}, দেখা হবে অন্য দিন 🥲"
        )

# ✅ Main runner
if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(ChatMemberHandler(welcome_member, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(ChatMemberHandler(farewell_member, ChatMemberHandler.CHAT_MEMBER))

    print("✅ Bot is running... /info, /report, welcome & leave active")
    app.run_polling()
