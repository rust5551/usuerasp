import requests
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
from datetime import datetime, timedelta 

BOT_TOKEN = os.environ['BOT_TOKEN']



# startDate = "01.09.2024"
# endDate = "08.09.2024"
def getrasp(startDate, endDate):
    rasp = requests.get(f"https://www.usue.ru/schedule/?t=0.01851820357425471&action=show&startDate={startDate.strftime('%d.%m.%Y')}&endDate={endDate.strftime('%d.%m.%Y')}&group=%D0%98%D0%92%D0%A2-24-1")
    rjson = rasp.json()
    output = []
    for day in rjson:
        out = f"{day['weekDay']} {day['date']}"
        day["pairs"] = day["pairs"][:8]

        for pair in day["pairs"]:
            if pair['schedulePairs']:
                out += f"\n\n{pair['schedulePairs'][0]['comm'][:-5]} {pair['N']} пара:"
            else:
                out += f"\n\n{pair['time']} {pair['N']} пара:"
            for sched in pair["schedulePairs"]:
                out += f"\n{sched['subject']} {sched['aud']} {sched['group'][9:]}"
        out += '\n'
        output.append(out)

    megaout = ""
    for i in output:
        megaout += i
        megaout += "\n—————————————————————————————————\n"
    return megaout

def logger(update):
    with open("logs.txt", "a+", encoding="UTF-8") as f:
        f.write(f"[{update.effective_user.first_name} | @{update.effective_user.username} | {update.message.date.astimezone()}]   {update.message.text} \n ——————————————— \n")

async def rasp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger(update)
    if context.args:
        try:
            startDate = datetime.strptime(context.args[0], "%d.%m.%Y")
            endDate = startDate + timedelta(days=int(context.args[1]))
            print(startDate, endDate)
            #getrasp(startDate, endDate)
        except:
            print("damn bro")
            startDate = datetime.today()
            endDate = startDate + timedelta(days=7)
    else:
        startDate = datetime.today()
        endDate = startDate + timedelta(days=7)
    #print(startDate, endDate)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"```Расписание \n{getrasp(startDate, endDate)}```", parse_mode="MarkdownV2")

async def rasptd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger(update)
    startDate = datetime.today()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"```Расписание \n{getrasp(startDate, startDate)}```", parse_mode="MarkdownV2")

async def rasptm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger(update)
    startDate = datetime.today() + timedelta(days=1)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"```Расписание \n{getrasp(startDate, startDate)}```", parse_mode="MarkdownV2")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger(update)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Помощь – /help")

async def get_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger(update)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Используйте /rasp 02.09.2024 n, где n это число дней на которое необходимо расписание \n\nЛибо просто /rasp отправляет расписание на неделю вперёд")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger(update)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Помощь – /help")


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    echo_handler = MessageHandler(filters.TEXT and (~filters.COMMAND), echo)
    rasp_handler = CommandHandler('rasp', rasp)
    rasptd_handler = CommandHandler('rasptd', rasptd)
    rasptm_handler = CommandHandler('rasptm', rasptm)
    help_handler = CommandHandler('help', get_help)
    start_handler = CommandHandler('start', start)

    application.add_handler(echo_handler)
    application.add_handler(rasp_handler)
    application.add_handler(rasptd_handler)
    application.add_handler(rasptm_handler)
    application.add_handler(help_handler)
    application.add_handler(start_handler)


    application.run_polling()