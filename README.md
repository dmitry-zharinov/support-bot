# Бот службы поддержки 
  
### Установка
1. Предварительно должен быть установлен Python3.
2. Для установки зависимостей, используйте команду pip (или pip3, если есть конфликт с Python2) :
```
pip install -r requirements.txt
```
3. Необходимо [зарегистрировать бота и получить его API-токен](https://telegram.me/BotFather)
4. В директории скрипта создайте файл `.env` и укажите в нём следующие данные:

- `TG_BOT_TOKEN` — токен для Telegram-бота, полученный от Bot Father.
- `DIALOGFLOW_PROJECT_ID` — идентификатор проекта в DialogFlow [см. документацию](https://cloud.google.com/dialogflow/es/docs/quick/setup) 
- `DIALOGFLOW_SESSION_ID` — уникальная строка (например, имя телеграм-бота). 
- `GOOGLE_APPLICATION_CREDENTIALS` - путь до файла с ключами в формате `.json` - [см. документацию](https://cloud.google.com/docs/authentication/client-libraries)
- `VK_GROUP_TOKEN` - токен группы ВКонтакте - [см. документацию](https://dev.vk.com/api/access-token/getting-started#%D0%9A%D0%BB%D1%8E%D1%87%20%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0%20%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D1%81%D1%82%D0%B2%D0%B0)
- `TG_CHAT_ID` — id чата, куда будут отправляться логи (можно узнать у @userinfobot).


### Запуск Telegram бота 
```
$ python tg_bot.py
```

### Запуск бота Вконтакте 
```
$ python vk_bot.py
```

### Обучение DialogFlow 
Для того, чтобы обучить бота тренировочным фразам и ответам, создайте .json файл в следующем формате:
```
{
    "Намерение": {
        "questions": [
            "Вопрос",
        ],
        "answer": "Ответ"
    },
}

```

Запустите скрипт для обучения Dialogflow, указав путь к json файлу:
```
$ python train_dialogflow.py ./questions.json
```