import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialogflow import detect_intent_texts

logger = logging.getLogger('tg-bot')


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Здравствуйте!')


def reply_user(update: Update, context: CallbackContext):
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    session_id = os.getenv('DIALOGFLOW_SESSION_ID')
    fulfillment_text = detect_intent_texts(
        project_id,
        session_id,
        update.message.text,
        'ru-RU'
    ).fulfillment_text
    update.message.reply_text(fulfillment_text)


def run_bot(token):
    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, reply_user)
    )
    updater.start_polling()
    updater.idle()


def main():
    load_dotenv()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    token = os.getenv('TG_BOT_TOKEN')
    os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    run_bot(token)
    try:
        run_bot(token)
    except Exception as err:
        logger.exception(err)


if __name__ == '__main__':
    main()
