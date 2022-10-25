import logging

from environs import Env
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

logger = logging.getLogger(__name__)


def start(update, _):
    menu_keyboard = [
        [
            InlineKeyboardButton('Новый вопрос', callback_data='1'),
            InlineKeyboardButton('Сдаться', callback_data='2'),
        ],
        [
            InlineKeyboardButton('Мой счет', callback_data='3')
        ],
    ]
    reply_markup = InlineKeyboardMarkup(menu_keyboard)
    update.message.reply_text('Привет! Я бот для викторин.', reply_markup=reply_markup)


def echo(update, _):
    update.message.reply_text(update.message.text)


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    env = Env()
    env.read_env()
    tg_token = env('TG_TOKEN')
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
