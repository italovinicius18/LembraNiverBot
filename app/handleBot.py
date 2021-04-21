"""
This script connect the bot and get all of the messages
"""

import os
from dotenv import load_dotenv

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

import pytz

from pprint import pprint

from helperFunctions import *
from dbController import *

# Credentials
load_dotenv('.env')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

USER, BIRTHDAY_DATA = range(2)


def start(update: Update, _: CallbackContext) -> None:

    update.message.reply_text(
        'Olá, meu nome é LembraNiverBot. Eu vou te ajudar a lembrar a data de aniversário de todos seus conhecidos\n'
        'Basta apenas me enviar o comando:\n /add NOME DD\MM ou /add NOME DD\MM\YYYY\n'
        'Quando for o aniversário de algum destes conhecidos, eu te enviarei uma mensagem te notificando 🎂🎇'
    )


def add(update: Update, context: CallbackContext) -> None:

    USER = update.message.from_user

    haveYear = False

    try:
        # args[0] should contain the time for the timer in seconds
        full_name = context.args[0:-1]
        birthday = context.args[-1]

        valid_name, name = check_name(full_name)
        valid_date, birthday = check_birthday(birthday)

        if not valid_name:
            text = 'Por favor, adicione um nome correto 😔\n'
        elif not valid_date:
            text = 'Por favor, adicione uma data correta 😔\n'
        else:
            text = f'{USER.first_name} adicionamos o aniversário que você solicitou 🎁'

        data = {
            'telegram_id':
            USER['id'],
            'name':
            USER['first_name'],
            'friends': [{
                'name': ' '.join(full_name),
                'birthday': {
                    'day': birthday.day,
                    'month': birthday.month,
                    'year': birthday.year
                }
            }]
        }

        insert_birthday(data)

        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text(
            'Desculpe, mas a formato do seu comando está errado 😔\n'
            'Use o comando: /add NOME DD/MM ou /add NOME DD/MM/AAAA\n')


def send_congratulations(context: CallbackContext) -> None:
    """Send the alarm message."""
    users = get_all_today_birthdays()

    for data in users:

        pprint(data)

        user_name = data['name']
        friend_name = data['friends']['name']
        user_id = data['telegram_id']

        text = 'Olá, {}, hoje é o aniversário do(a) {}, deseje felicidades para ele(a) 🎉'.format(
            user_name, friend_name)

        context.bot.sendMessage(user_id, text=text)


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAM_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('add', add))

    # Set the daily jobs to remind the user their frieds birthdays
    job = updater.job_queue
    job_daily = job.run_daily(send_congratulations,
                              time=datetime.time(
                                  hour=5,
                                  tzinfo=pytz.timezone('America/Sao_Paulo')))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()