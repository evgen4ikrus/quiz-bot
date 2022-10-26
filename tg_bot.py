import logging

import telegram
from environs import Env
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from quiz_helpers import get_random_question
from redis_tools import auth_redis
from functools import partial


logger = logging.getLogger('tg_bot')


def start(bot, update):
    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    chat_id = str(update.effective_user.id)
    bot.send_message(chat_id=chat_id, text='Привет, я бот для викторин!', reply_markup=reply_markup)


def echo(bot, update, redis_db):
    message_text = update.message.text
    chat_id = str(update.effective_user.id)
    if message_text == 'Новый вопрос':
        question = get_random_question()
        update.message.reply_text(question)
        redis_db.set(chat_id, question)


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    env = Env()
    env.read_env()
    redis_address = env('REDIS_ADDRESS')
    redis_port = env('REDIS_PORT')
    redis_password = env('REDIS_PASSWORD')
    tg_token = env('TG_TOKEN')

    quiz_db = auth_redis(redis_address, redis_port, redis_password)
    quiz_db.flushall()
    
    updater = Updater(tg_token)

    dp = updater.dispatcher
    echo_with_args = partial(echo, redis_db=quiz_db)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_with_args))

    updater.start_polling()
    logger.info('TG бот запущен')

    updater.idle()


if __name__ == '__main__':
    main()
