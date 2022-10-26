import logging
import os
import random

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from detect_intent_texts import detect_intent_texts

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def echo(event, vk_api):
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


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv('VK_GROUP_TOKEN')
    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
                echo(event, vk_api)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)
