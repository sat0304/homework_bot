## Python telegram bot for Yandex.Homework 
...
Telegram-бот на Python использующий API Яндекс.Домашка для отслеживания статусов сданных работ
...
Бот раз в 10 минут опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы; при обновлении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram; логирует свою работу и сообщает о важных проблемах сообщением в Telegram.

Клонировать репозиторий и перейти в него в командной строке: git clone https://github.com/alferius/homework_bot.git cd homework_bot

Cоздать и активировать виртуальное окружение: python3 -m venv env source env/bin/activate

Установить зависимости из файла requirements.txt: python3 -m pip install --upgrade pip pip install -r requirements.txt

Запустить проект: python3 manage.py runserver
