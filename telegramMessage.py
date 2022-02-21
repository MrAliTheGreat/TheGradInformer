from datetime import datetime
from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram import Update
import os

from main import runMain

lastFetchedResult = ""

updater = Updater(
    token = os.environ.get("TELEGRAM_TOKEN"),
    use_context = True
)

def start(update : Update, ctx : CallbackContext):
    intervalInMinutes = 120

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
    finalMessage, lastFetchedResult = runMain(lastFetchedResult)
    if(finalMessage):
        ctx.bot.send_message(
            chat_id = ctx.job.context,
            text = finalMessage
        )

    print("Log: New message was sent at " + str(datetime.now()))

def live(update : Update, ctx : CallbackContext):
    ctx.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "TheGradInformer is live!"
    )


updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("live", live))


updater.start_polling()
updater.idle()

