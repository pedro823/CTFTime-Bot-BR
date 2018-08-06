import requests
import daemon
import time
import telepot
from datetime import datetime
from dateutil import tz
from telepot.loop import MessageLoop

strip_timezone = lambda time_str: time_str[:19]

current_time = lambda: str(int(time.time()))

craft_message_from_ctf = lambda ctf: '''
%s
%s
Inicia em: %s
Termina em: %s
''' % (ctf['title'], 
       ctf['url'], 
       convert_time(strip_timezone(ctf['start'])), 
       convert_time(strip_timezone(ctf['finish'])))

def convert_time(time):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/Sao_Paulo')
    utc = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)

    # Converts time zone
    brazil = utc.astimezone(to_zone)
    brazil = brazil.strftime("%d/%m/%Y %H:%M")
    return brazil


def get_ctfs():
    resp = requests.get(URL, params=PARAMS, headers=HEADERS)
    response_items = resp.json()
    message = '*Próximos CTFs:*\n'
    for ctf in response_items:
        message += craft_message_from_ctf(ctf)
    return message


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    if command and '/ctfs' in command:
        bot.sendMessage(chat_id, get_ctfs(), parse_mode='Markdown')

URL = 'https://ctftime.org/api/v1/events/?'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
PARAMS = dict(
    limit='5',
    start=current_time(),
    finish=str(int(current_time()) + 2629800)
)
API_KEY = 'Insira sua API key aqui'

with daemon.DaemonContext():
    bot = telepot.Bot(API_KEY)
    print('Começando a escutar por requests...')
    MessageLoop(bot, handle).run_forever()
