from TgBot import bot, BuildMsg
from telethon import events, Button

@bot.on(events.NewMessage(pattern='^/start'))
async def on_start(event):
    ID = event.sender_id
    text = BuildMsg(ID, 'PM_START_MSG')
    buttons = [
        [Button.url(BuildMsg(ID, 'DEV_ACCOUNT_LINK'), 'https://telegram.dog/SastaDev')],
        [Button.url(BuildMsg(ID, 'UPDATES_CHANNEL'), 'https://telegram.dog/SastaNetwork')]
        ]
    await event.reply(text, buttons=buttons)