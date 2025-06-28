from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

BOT_TOKEN = '7632441744:AAGwpaUtsjO-S4Bj9OuD8MQKTNBDCeWiah0'

# শুধু অ্যাডমিনদের ইউজার আইডি বসাও এখানে
ADMINS = [
    7949308405,  # তোমার আইডি বসাও
    987654321,  # আরেকজন অ্যাডমিন
]

# রোস্ট লিস্ট (বগুড়া ক্রাশ অ্যান্ড কনফেশন স্টাইল)
roasts = [
    "😂 @{user} নাকি বগুড়ার ক্রাশ! মেয়েরা দেখলে বলে: 'এই যে ভাইয়া, রাস্তা ছাড়েন!'",
    "🤣 @{user} এর ক্রাশ বলে: 'তোমাকে দেখে আমি আমার ex এর কথা মনে করি।'",
    "😆 @{user} এত এক্স বানিয়েছে, এখন প্রেম করতে গেলে আগে পুলিশ ক্লিয়ারেন্স লাগে!",
    "🥲 @{user} কনফেশন লিখতে গিয়েছিল, গ্রুপ হঠাৎ সাইলেন্ট হয়ে গেল।",
    "👀 @{user} এর ক্রাশ এখন অন্যের বউ!",
    "💔 @{user} নাকি প্রেম করে? ওর তো crush-ই ওকে block করে রাখে!",
    "🫣 @{user} এর কনফেশন পড়ে মেয়েরা বলতেছে: 'এই ভাইটা নাহি থামবে তো?'",
    "😹 @{user} এর কনফেশন দেখে বগুড়ার মেয়েরা বগুড়া ছাড়ছে!",
    "😎 @{user} প্রেমে এমন pro যে, আজকে কনফেশন দেয়, কালকে unfriend!",
    "🙃 @{user} এর ক্রাশ reply না দিলে বটকে কনফেশন দেয়!",
    "🤣 @{user} এক্স এর সাথে দেখা হলে বলে: 'মাফ করে দে, জীবনে ভুল হইছে।'",
    "😂 @{user} নাকি এক মেয়েকে ৩ বার কনফেশন দিয়েছে, মেয়ে reply দিলো: OK BRO!",
    "😆 @{user} এর বগুড়া স্টাইল প্রেম: online শুধু, offline নাই!",
    "🥴 @{user} কে দেখলে বগুড়ার মেয়েরা বলে: 'এটা আবার কার crush?'",
    "🔥 @{user} এর কনফেশন এত জোস যে গ্রুপের এডমিনও হেসে কেঁদেছে।",
    "💀 @{user} প্রেমে পড়ে কনফেশন দিলো, মেয়ে বললো 'আপনি তো আমার ভাইয়ের মতো!'",
    "😵 @{user} নাকি এমন প্রেমিক, একদিনে তিনটা breakup!",
    "😆 @{user} কে tag দিলেই ex, crush আর gf একসাথে লাফায়!",
    "👻 @{user} crush কে impress করতে গিয়ে নিজের নাম ভুলে গেছে।",
    "💘 @{user} এর প্রেম মানে: ‘তুমি reply দিলে আমি poem লিখবো, না দিলে song!’"
]

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # শুধুমাত্র ADMINS পারবে
    if user_id not in ADMINS:
        await update.message.reply_text("⛔ এই কমান্ডটি শুধুমাত্র অ্যাডমিনদের জন্য।")
        return

    if len(context.args) != 1:
        await update.message.reply_text("ব্যবহার: /news @username")
        return

    target_username = context.args[0]

    if not target_username.startswith('@'):
        target_username = '@' + target_username

    roast_line = random.choice(roasts).replace("{user}", target_username.lstrip('@'))
    await update.message.reply_text(roast_line)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("news", news))

    print("🔥 বগুড়া ক্রাশ বট চালু!")
    app.run_polling()
