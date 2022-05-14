## Телеграм бот на Python для Яндекс.Практикум
```
Telegram-бот на Python использующий API Яндекс.Практикум для отслеживания статусов сданных работ
```
Как работает бот?
```
Бот раз в 10 минут опрашивает API Практикум.Практикум и проверяет статус отправленной на проверку домашней работы. При изменении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram.
Кроме этого отслеживает свою работу и сообщает о важных проблемах в Telegram.
```
### Технологии
```
Python 3.10
Django 2.2.19
Django REST Framework 3.12.4
python-dotenv 0.19.0
python-telegram-bot 13.7
requests 2.26.0
```
### Запуск проекта
Клонировать репозиторий и перейти в него в командной строке: 
```
git clone https://github.com/sat0304/homework_bot.git 
cd homework_bot
```
Cоздать и активировать виртуальное окружение: 
```
python3 -m venv env 
source env/bin/activate
```
Установить зависимости из файла requirements.txt: 
```
python3 -m pip install --upgrade pip 
pip install -r requirements.txt
```
Запустить проект: 
```
python3 manage.py runserver
```
