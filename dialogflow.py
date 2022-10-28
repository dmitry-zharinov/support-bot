import argparse
import json
import logging
import os

from dotenv import load_dotenv
from google.cloud import dialogflow

logger = logging.getLogger('dialogflow_bot')


def create_intent(project_id,
                  display_name,
                  training_phrases_parts,
                  message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    logger.info(f'Intent created: {response}')


def detect_intent_texts(project_id, session_id, texts, language_code="ru-RU"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
        text=texts,
        language_code=language_code
    )

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result


def argparser():
    parser = argparse.ArgumentParser(
        description="Adds new questions and answers to DialogFlow"
    )
    parser.add_argument("path", help="Path to .json file")
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    load_dotenv()
    args = argparser()

    try:
        with open(args.path, "r", encoding='utf8') as file:
            intents = json.loads(file.read())

    except (FileNotFoundError, PermissionError) as err:
        exit(err)

    for intent, phrases in intents.items():
        create_intent(
            os.getenv('DIALOGFLOW_PROJECT_ID'),
            intent,
            phrases["questions"],
            [phrases["answer"]],
        )
