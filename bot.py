from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext
import random

TOKEN = "8506949404:AAHCp2ABuL5ZXCFcUGn5bhk0d9PcfpmYfYo"

ADMIN_ID = 8437585105  # O'Z TELEGRAM ID INGNI YOZ
CHANNEL_USERNAME = "@alishern1_youtuber"  # KANALING

participants = []
contest_active = False
max_users = 0


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🎉 Konkurs botga xush kelibsiz!\n\n"
        "Qatnashish uchun: /join"
    )


def create_contest(update: Update, context: CallbackContext):
    global contest_active, participants, max_users

    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) != 1:
        update.message.reply_text("❌ Foydalanish: /create 50")
        return

    max_users = int(context.args[0])
    participants = []
    contest_active = True

    update.message.reply_text(
        f"✅ Konkurs boshlandi!\n"
        f"👥 Maksimal qatnashchi: {max_users}\n\n"
        f"Qatnashish uchun: /join"
    )


def join(update: Update, context: CallbackContext):
    global contest_active

    if not contest_active:
        update.message.reply_text("❌ Hozir aktiv konkurs yo‘q")
        return

    user = update.effective_user

    if user.id in participants:
        update.message.reply_text("⚠️ Siz allaqachon qatnashyapsiz")
        return

    participants.append(user.id)

    update.message.reply_text(
        f"✅ Qabul qilindingiz!\n"
        f"👥 Jami: {len(participants)}/{max_users}"
    )

    if len(participants) >= max_users:
        end_contest(update, context)


def end_contest(update: Update, context: CallbackContext):
    global contest_active

    if update.effective_user.id != ADMIN_ID:
        return

    if not participants:
        update.message.reply_text("❌ Qatnashchilar yo‘q")
        return

    winner_id = random.choice(participants)
    contest_active = False

    context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=f"🏆 <b>KONKURS G‘OLIBI</b>\n\n"
             f"🎉 <a href='tg://user?id={winner_id}'>G‘olib profiliga o‘tish</a>",
        parse_mode=ParseMode.HTML
    )

    update.message.reply_text("✅ Konkurs yakunlandi")


def stop_contest(update: Update, context: CallbackContext):
    global contest_active
    if update.effective_user.id == ADMIN_ID:
        contest_active = False
        update.message.reply_text("⛔ Konkurs to‘xtatildi")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("create", create_contest))
    dp.add_handler(CommandHandler("join", join))
    dp.add_handler(CommandHandler("end", end_contest))
    dp.add_handler(CommandHandler("stop", stop_contest))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
