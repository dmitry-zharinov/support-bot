import logging
import os
import random

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow import detect_intent_texts
from bot_logging import TelegramLogsHandler

logger = logging.getLogger('vk-bot')


def answer_user(event, vk_api):
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    session_id = os.getenv('DIALOGFLOW_SESSION_ID')
    answer = detect_intent_texts(
        project_id,
        session_id,
        event.text,
    )
    if answer.intent.is_fallback:
        return

    vk_api.messages.send(
        user_id=event.user_id,
        message=answer.fulfillment_text,
        random_id=random.randint(1, 1000)
    )


def run_bot(token):
    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer_user(event, vk_api)


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.getenv('VK_GROUP_TOKEN')
    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')

    logging.basicConfig(level=logging.INFO)
    logger.addHandler(
        TelegramLogsHandler(tg_bot_token, tg_chat_id)
    )

    try:
        run_bot(vk_token)
    except Exception as err:
        logger.exception(err)
