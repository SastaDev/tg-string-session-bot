from TgBot import bot, database, BuildMsg
from telethon import events

@bot.on(events.NewMessage(pattern='^/setlang'))
async def on_set_lang(event):
    ID = event.sender_id
    msg = event.raw_text.split()
    if len(msg) <= 1:
        pass
    new_lang = msg[1].upper()
    database.set_lang(ID, new_lang)
    await event.reply(BuildMsg(ID, 'NEW_LANG_SET').format(new_lang))