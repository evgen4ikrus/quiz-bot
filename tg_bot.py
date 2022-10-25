import logging

import telegram
from environs import Env
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

logger = logging.getLogger(__name__)


def start(bot, update):
    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    chat_id = str(update.effective_user.id)
    bot.send_message(chat_id=chat_id, text='Привет, я бот для викторин!', reply_markup=reply_markup)


def echo(bot, update):
    update.message.reply_text(update.message.text)


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    env = Env()
    env.read_env()
    tg_token = env('TG_TOKEN')
    updater = Updater(tg_token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
