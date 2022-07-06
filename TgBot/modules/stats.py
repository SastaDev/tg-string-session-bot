from TgBot import bot, config, database
from telethon import events

@bot.on(events.NewMessage)
async def on_new_message(event):
    if not event.is_private:
        return
    ID = event.sender_id
    if ID not in database.get_total_users_list():
        database.add_user(ID)

@bot.on(events.NewMessage(pattern='/stats'))
async def on_stats(event):
    ID = event.sender_id
    bot_owners = config['BOT_OWNERS']
    devs = config['DEVS']
    special_users = config['SPECIAL_USERS']
    if ID not in bot_owners and ID not in devs and ID not in special_users:
        return
    total_users = database.get_total_users_list()
    tnssc = database.get_total_ss_created_list()
    text = f'''
<b>Statistic:</b>

<b>Total Users:</b> <code>{len(total_users)}</code><i>.</i>
<b>Total Numbers of String Sessions Created:</b> <code>{len(tnssc)}</code><i>.</i>
    '''
    await event.reply(text)