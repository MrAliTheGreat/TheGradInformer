from datetime import datetime
from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram import Update
import os

from dotenv import load_dotenv

load_dotenv()

from main import runMain


def createLogFormat(numMessages):
    if(numMessages == 1):
        return "Log: 1 new message was sent at " + str(datetime.now())
    elif(numMessages > 1):
        return "Log: " + str(numMessages) + " new messages were sent at " + str(datetime.now())

    return "Log: No new result was fetched at " + str(datetime.now())



lastFetchedResult = ""

updater = Updater(
    token = os.environ.get("TELEGRAM_TOKEN"),
    use_context = True
)

def start(update : Update, ctx : CallbackContext):
    intervalInMinutes = 1

    ctx.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Hello I'm TheGradInformer and I'm at your service!"
    )

    ctx.job_queue.run_repeating(
        resultFetcher,
        interval = intervalInMinutes * 60,
        context = update.effective_chat.id
    )

def resultFetcher(ctx : CallbackContext):
    global lastFetchedResult
    messages, lastFetchedResult = runMain(lastFetchedResult)

    for message in messages:
        ctx.bot.send_message(
            chat_id = ctx.job.context,
            text = message
        )

    print(createLogFormat(len(messages)))

def live(update : Update, ctx : CallbackContext):
    ctx.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "TheGradInformer is live!"
    )


updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("live", live))


updater.start_polling()
updater.idle()

