import logging

import telegram
from environs import Env
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from quiz_helpers import get_random_question


logger = logging.getLogger('tg_bot')


def start(bot, update):
    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    chat_id = str(update.effective_user.id)
    bot.send_message(chat_id=chat_id, text='Привет, я бот для викторин!', reply_markup=reply_markup)


def echo(bot, update):
    message_text = update.message.text
    if message_text == 'Новый вопрос':
        question = get_random_question()
        update.message.reply_text(question)


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
    logger.info('TG бот запущен')

    updater.idle()


if __name__ == '__main__':
    main()
