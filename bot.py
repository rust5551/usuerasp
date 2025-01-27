import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
import telegram
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
from datetime import datetime, timedelta 
from schedule import make_it_pretty
# from database import add_user, change_group

def logger(update):
    with open("logs.txt", "a+", encoding="UTF-8") as f:
        f.write(f"[{update.effective_user.first_name} | @{update.effective_user.username} | {update.message.date.astimezone()}]   {update.message.text} \n ——————————————— \n")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger(update)
    texts = {
        'На неделю': rasp,
        'На сегодня': rasptd,
        'На завтра': rasptm
    }
    try:
        await texts[update.effective_message.text](update, context)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите /start")
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=update.effective_message.text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger(update)
    reply_keyboard = [["На неделю", "На завтра", "На сегодня"]]

    await update.message.reply_text("Hello there", reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=False, input_field_placeholder="Получить расписание", resize_keyboard=True
    ))

async def rasp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger(update)
    start_date = datetime.today()
    end_date = start_date + timedelta(days=6)
    if context.args:
        try:
            start_date = datetime.strptime(context.args[0], "%d.%m.%Y")
            end_date = start_date + timedelta(days=int(context.args[1]))
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Использование: /rasp 01.01.2025 7")
            start_date = datetime.today()
            end_date = start_date + timedelta(days=6)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=make_it_pretty(start_date, end_date, "ИВТ-24-1"), parse_mode="HTML")

async def rasptd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger(update)
    start_date = datetime.today()
    end_date = start_date
    await context.bot.send_message(chat_id=update.effective_chat.id, text=make_it_pretty(start_date, end_date, "ИВТ-24-1"), parse_mode="HTML")

async def rasptm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger(update)
    start_date = datetime.today() + timedelta(days=1)
    end_date = start_date
    await context.bot.send_message(chat_id=update.effective_chat.id, text=make_it_pretty(start_date, end_date, "ИВТ-24-1"), parse_mode="HTML")


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    echo_handler = MessageHandler(filters.TEXT and (~filters.COMMAND), echo)
    start_handler = CommandHandler("start", start)
    rasp_handler = CommandHandler("rasp", rasp)
    rasptd_handler = CommandHandler("rasptd", rasptd)
    rasptm_handler = CommandHandler("rasptm", rasptm)

    application.add_handler(echo_handler)
    application.add_handler(start_handler)
    application.add_handler(rasp_handler)
    application.add_handler(rasptd_handler)
    application.add_handler(rasptm_handler)

    application.run_polling()