import logging
from functools import partial

import telegram
from environs import Env
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, RegexHandler, Updater)

from quiz_helpers import get_answer, get_random_question
from redis_tools import auth_redis


logger = logging.getLogger('tg_bot')


NEW_QUESTION, SOLUTION_ATTEMPT = range(2)


def start(bot, update):
    menu_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = telegram.ReplyKeyboardMarkup(menu_keyboard)
    update.message.reply_text('Привет, я бот для викторин! Нажми кнопку "Новый вопрос"', reply_markup=reply_markup)
    return NEW_QUESTION


def handle_new_question_request(bot, update, redis_db):
    menu_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = telegram.ReplyKeyboardMarkup(menu_keyboard)
    chat_id = str(update.effective_user.id)
    question = get_random_question()
    redis_db.set(chat_id, question)
    update.message.reply_text(text=question, reply_markup=reply_markup)
    return SOLUTION_ATTEMPT


def handle_solution_attempt(bot, update, redis_db):
    menu_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = telegram.ReplyKeyboardMarkup(menu_keyboard)
    chat_id = str(update.effective_user.id)
    question = redis_db.get(chat_id)
    message_text = update.message.text
    if not question:
        return NEW_QUESTION
    answer = get_answer(question)
    if answer == message_text:
        update.message.reply_text('Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»',
                                  reply_markup=reply_markup)
        return NEW_QUESTION
    else:
        update.message.reply_text('Неправильно… Попробуешь ещё раз?', reply_markup=reply_markup)
        return SOLUTION_ATTEMPT


def handle_other_text(bot, update):
    menu_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = telegram.ReplyKeyboardMarkup(menu_keyboard)
    update.message.reply_text('Нажми на кнопку "Новый вопрос"', reply_markup=reply_markup)
    return NEW_QUESTION


def handle_defeat(bot, update, redis_db):
    chat_id = str(update.effective_user.id)
    question = redis_db.get(chat_id)
    if not question:
        return NEW_QUESTION
    answer = get_answer(question)
    update.message.reply_text(f'Правильный ответ: {answer}')
    handle_new_question_request(bot, update, redis_db=redis_db)


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
    handle_solution_attempt_with_args = partial(handle_solution_attempt, redis_db=quiz_db)
    handle_new_question_request_with_args = partial(handle_new_question_request, redis_db=quiz_db)
    handle_defeat_with_args = partial(handle_defeat, redis_db=quiz_db)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NEW_QUESTION: [RegexHandler('Новый вопрос', handle_new_question_request_with_args)],
            SOLUTION_ATTEMPT: [RegexHandler('Сдаться', handle_defeat_with_args),
                               MessageHandler(Filters.text, handle_solution_attempt_with_args)],
        },
        fallbacks=[MessageHandler(Filters.text, handle_other_text)]
    )
    dp.add_handler(conv_handler)

    updater.start_polling()
    logger.info('TG бот запущен')

    updater.idle()


if __name__ == '__main__':
    main()
