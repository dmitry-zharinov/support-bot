from dotenv import load_dotenv
import json
import argparse
import os


def load_json(filepath):
    with open(filepath, "r", encoding='utf8') as file:
        return json.loads(file.read())


def create_intent(project_id,
                  display_name,
                  training_phrases_parts,
                  message_texts):
    from google.cloud import dialogflow

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

    print(f"Intent created: {response}")


def argparser():
    parser = argparse.ArgumentParser(
        description="Adds new questions and answers to DialogFlow"
    )
    parser.add_argument("path", help="Path to .json file")
    return parser.parse_args()


if __name__ == "__main__":
    load_dotenv()
    args = argparser()

    try:
        intents = load_json(args.path)
    except (FileNotFoundError, PermissionError) as err:
        exit(err)

    for intent, phrases in intents.items():
        create_intent(
            os.getenv('DIALOGFLOW_PROJECT_ID'),
            intent,
            phrases["questions"],
            [phrases["answer"]],
        )
