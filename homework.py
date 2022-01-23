import logging
import os
import requests
import sys
import time as t

from dotenv import load_dotenv
from http import HTTPStatus
from telegram import Bot


load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN_ENV')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN_ENV')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID_ENV')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)s, %(message)s'
)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def send_message(bot, message):
    """Отправка сообщения в Телеграм."""
    bot.send_message(TELEGRAM_CHAT_ID, message)
    logger.info('Сообщение для sat0304_bot отправлено')


def get_api_answer(current_timestamp):
    """Получение ответа API Практикум.Домашка."""
    timestamp = current_timestamp
    params = {'from_date': timestamp}
    if params['from_date'] == current_timestamp:
        response = requests.get(url=ENDPOINT, headers=HEADERS, params=params)
    if response.status_code == HTTPStatus.OK:
        logger.info('Сайт API Практикум.Домашка доступен')
        if response is not None:
            logger.info('Получен ответ от API Практикум.Домашка')
            return response.json()
        else:
            logger.error('Получен пустой ответ API Практикум.Домашка')
    else:
        raise SystemError(
            f'Недоступен API Практикум.Домашка {response.status_code}'
        )


def check_response(response):
    """Проверка ответа API сайта Практикум.Домашка."""
    try:
        if type(response) == dict:
            cur_date = response['current_date']
            logger.info(f'Дата проверки API Практикум.Домашка {cur_date}')
            homeworks = response['homeworks']
            try:
                if type(homeworks) == list:
                    logger.info('Получен список от API Практикум.Домашка')
                    return homeworks
            except TypeError('Получен пустой список'):
                logger.error('Получен пустой список от API Практикум.Домашка')
                return []
    except TypeError('Получен неправильный результат'):
        logger.error('Получен неправильный результат')
        return []


def parse_status(homework):
    """Извлечение данных из ответа API сайта Практикум.Домашка."""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_name is not None:
        if ((homework_status is not None)
            and (homework_status in HOMEWORK_STATUSES)):
            verdict = HOMEWORK_STATUSES.get(homework_status)
            logger.info(
                f'Изменился статус проверки работы'
                f'"{homework_name}". {verdict}'
            )
            return (
                f'Изменился cтатус проверки работы'
                f'"{homework_name}". {verdict}'
            )
        else:
            logger.error(f'Некорректный статус проверки на'
                f'API Практикум.Домашка')
            return ('Не изменился cтатус проверки работы')
    else:
        logger.error('Некорректное имя работы на API Практикум.Домашка')
        return ('Не изменился cтатус проверки работы')


def check_tokens():
    """Проверяем доступность переменных окружения."""
    token_error = ('Отсутствует переменная окружения: ')
    token = True
    if PRACTICUM_TOKEN is None:
        token = False
        logger.critical(f'{token_error}PRACTICUM_TOKEN')
    elif TELEGRAM_TOKEN is None:
        token = False
        logger.critical(f'{token_error}TELEGRAM_TOKEN')
    elif TELEGRAM_CHAT_ID is None:
        token = False
        logger.critical(f'{token_error}TELEGRAM_CHAT_ID')
    return token


def main():
    """Основная логика работы бота."""
    if check_tokens():
        bot = Bot(token=TELEGRAM_TOKEN)
        current_timestamp = int(t.time())
        old_homework = None
    else:
        sys.exit(1)
    while True:
        try:
            response = get_api_answer(current_timestamp)
            current_timestamp = response.get('current_date')
            homework = check_response(response)
            old_error = None
            if len(homework) > 0:
                homework_1 = parse_status(homework[0])
                if homework_1 != old_homework:
                    logger.info(
                        f'Изменился статус проверки работы {homework_1}'
                    )
                    old_homework = homework_1
                    send_message(bot, f'Изменился {homework_1}')
            t.sleep(RETRY_TIME)
        except Exception as error:
            logger.error(f'Сбой в работе программы: {error}')
            if error != old_error:
                old_error = error
                message = f'Сбой в работе программы: {error}'
                send_message(bot, message)
                t.sleep(RETRY_TIME)
        else:
            logger.debug('Ошибок нет: бот работает')
            logger.debug(f'Неизменный статус проверки {old_homework}')


if __name__ == '__main__':
    main()
