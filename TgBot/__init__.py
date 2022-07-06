from telethon import TelegramClient
from . import database
import pymongo
import random
import json
import dns

config = json.loads(open('config.json', 'r').read())
dialogues = json.loads(open('dialogues.json', 'r').read())

API_ID = config['API_ID']
API_HASH = config['API_HASH']
BOT_TOKEN = config['BOT_TOKEN']
SESSION_FILE_NAME = config['SESSION_FILE_NAME']
MONGO_DB_URI = config['MONGO_DB_URI']

bot = TelegramClient(SESSION_FILE_NAME, api_id=API_ID, api_hash=API_HASH)

bot.parse_mode = 'html'

dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

database = database.MongoDB(CONNECTION_URI=MONGO_DB_URI)

def BuildMsg(ID, index):
    lang = database.get_lang(str(ID))
    if lang is None:
        lang = random.choice(config['BY_DEFAULT_LANGS'])
    return random.choice(dialogues[lang][index])

from . import modules
