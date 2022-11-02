import logging

import vk_api as vk
from environs import Env
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id

logger = logging.getLogger('vk_bot')


def echo(event, vk_api, keyboard):
    vk_api.messages.send(
        peer_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=event.text
    )


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    env = Env()
    env.read_env()
    vk_group_token = env('VK_GROUP_TOKEN')
    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    menu_keyboard = VkKeyboard(one_time=True)
    menu_keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    menu_keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    menu_keyboard.add_line()
    menu_keyboard.add_button('Мой счет', color=VkKeyboardColor.PRIMARY)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api, keyboard=menu_keyboard)


if __name__ == "__main__":
    main()
