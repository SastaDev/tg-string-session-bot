from TgBot import bot, database, BuildMsg, config
from telethon import events, Button, TelegramClient
from telethon.sessions import StringSession
import telethon

from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)

data_cache = {}

@bot.on(events.NewMessage(pattern='^/create'))
async def on_create(event):
    ID = event.sender_id
    if database.is_blacklisted(ID):
        await event.reply(BuildMsg(ID, 'BLACKLISTED_USERS_CANNOT_VERIFY'))
        return
    data_cache[ID] = {
        'API_ID': None,
        'API_HASH': None,
        'PHONE_NUMBER': None,
        'LOGIN_CODE': None,
        'TWO_STEP_VERIFICATION_PASSWORD': None
    }
    buttons = [
        [Button.inline('Telethon', b'telethonlibrary'), Button.inline('Pyrogram', b'pyrogramlibrary')]
        ]
    await event.reply(BuildMsg(ID, 'CHOOSE_LIBRARY'), buttons=buttons)

@bot.on(events.CallbackQuery)
async def library_callback(event):
    c_data = event.data
    if c_data == b'telethonlibrary':
        await next_step(event, library='telethon')
    elif c_data == b'pyrogramlibrary':
        await next_step(event, library='pyrogram')

async def next_step(event, library):
    ID = event.sender_id
    if ID not in list(data_cache.keys()):
        try:
            await event.answer(BuildMsg(ID, 'USE_CREATE_COMMAND'), alert=True)
        except:
            await event.reply(BuildMsg(ID, 'USE_CREATE_COMMAND'))
        return
    if data_cache[ID]['API_ID'] is None:
        async with bot.conversation(event.chat, total_timeout=config['TOTAL_TIMEOUT'], exclusive=False) as conv:
                await conv.send_message(BuildMsg(ID, 'SEND_API_ID'), buttons=Button.force_reply())
                try:
                    response = await conv.get_response()
                    if not response.raw_text.isdigit():
                        await event.respond(BuildMsg(ID, 'INT_ONLY'))
                        await next_step(event, library='telethon')
                        return
                    data_cache[ID]['API_ID'] = int(response.raw_text)
                except:
                    await conv.send_message(BuildMsg(ID, 'TOO_SLOW_STARTOVER'))
                    del data_cache[ID]
                    return
                await next_step(event, library='telethon')
    elif data_cache[ID]['API_HASH'] is None:
        async with bot.conversation(event.chat, exclusive=False) as conv:
                await conv.send_message(BuildMsg(ID, 'SEND_API_HASH'), buttons=Button.force_reply())
                try:
                    response = await conv.get_response()
                    if not response.raw_text.isalnum():
                        await event.respond(BuildMsg(ID, 'STRING_ONLY'))
                        await next_step(event, library='telethon')
                        return
                    data_cache[ID]['API_HASH'] = str(response.raw_text)
                except:
                    await conv.send_message(BuildMsg(ID, 'TOO_SLOW_STARTOVER'))
                    del data_cache[ID]
                    return
                await next_step(event, library='telethon')
    elif data_cache[ID]['PHONE_NUMBER'] is None:
        async with bot.conversation(event.chat, exclusive=False) as conv:
                await conv.send_message(BuildMsg(ID, 'SEND_PHONE_NUMBER'), buttons=Button.force_reply())
                try:
                    response = await conv.get_response()
                    r = response.raw_text.replace('+', '')
                    if not r.isdigit():
                        await event.respond(BuildMsg(ID, 'INT_ONLY'))
                        await next_step(event, library='telethon')
                        return
                    data_cache[ID]['PHONE_NUMBER'] = str(response.raw_text)
                except:
                    await conv.send_message(BuildMsg(ID, 'TOO_SLOW_STARTOVER'))
                    del data_cache[ID]
                    return
                await next_step(event, library='telethon')
    else:
        if library == 'telethon':
            await generate_telethon_string_session(event)
        elif library == 'pyrogram':
            await generate_pyrogram_string_session(event)

async def generate_telethon_string_session(event):
    ID = event.sender_id
    DATA = data_cache[ID]
    async with bot.conversation(event.chat, exclusive=False) as conv:
        UserClient = TelegramClient(StringSession(), api_id=DATA['API_ID'], api_hash=DATA['API_HASH'])
        await UserClient.connect()
        try:
            await event.respond(BuildMsg(ID, 'REQUESTING_LOGIN_CODE'))
            request_login_code = await UserClient.send_code_request(DATA['PHONE_NUMBER'])
        except telethon.errors.rpcerrorlist.ApiIdInvalidError:
            await event.respond(BuildMsg(ID, 'INVALID_API_ID_OR_INVALID_API_HASH'))
            data_cache[ID]['API_ID'] = None
            data_cache[ID]['API_HASH'] = None
            await next_step(event, library='telethon')
            return
        except telethon.errors.rpcerrorlist.PhoneNumberBannedError:
            await event.respond(BuildMsg(ID, 'PHONE_NUMBER_BANNED'))
            data_cache[ID]['PHONE_NUMBER'] = None
            return
        except telethon.errors.rpcerrorlist.PhoneNumberFloodError:
            await event.respond(BuildMsg(ID, 'PHONE_NUMBER_FLOOD_ERROR'))
            data_cache[ID]['PHONE_NUMBER'] = None
            return
        except telethon.errors.rpcerrorlist.PhoneNumberInvalidError:
            await event.respond(BuildMsg(ID, 'PHONE_NUMBER_INVALID'))
            data_cache[ID]['PHONE_NUMBER'] = None
            return
        except telethon.errors.rpcerrorlist.PhonePasswordFloodError:
            await event.respond(BuildMsg(ID, 'PHONE_PASSWORD_FLOOD_ERROR'))
            data_cache[ID]['PHONE_NUMBER'] = None
            return
        except Exception as e:
            await event.respond(BuildMsg(ID, 'ERROR_REPORT_IT').format(e))
            del data_cache[ID]
            return
        async with bot.conversation(event.chat, exclusive=False) as conv:
            await conv.send_message(BuildMsg(ID, 'SEND_LOGIN_CODE'), buttons=Button.force_reply())
            try:
                response = await conv.get_response()
                data_cache[ID]['LOGIN_CODE'] = DATA['LOGIN_CODE'] = int(response.raw_text)
            except:
                await conv.send_message(BuildMsg(ID, 'TOO_SLOW_STARTOVER'))
                del data_cache[ID]
                return
        try:
            await UserClient.sign_in(DATA['PHONE_NUMBER'], code=DATA['LOGIN_CODE'])
        except telethon.errors.rpcerrorlist.SessionPasswordNeededError:
            async with bot.conversation(event.chat, exclusive=False) as conv:
                await conv.send_message(BuildMsg(ID, 'SEND_TWO_STEP_VERIFICATION_PASSWORD'), buttons=Button.force_reply())
                try:
                    response = await conv.get_response()
                    data_cache[ID]['TWO_STEP_VERIFICATION_PASSWORD'] = DATA['TWO_STEP_VERIFICATION_PASSWORD'] = str(response.raw_text)
                except:
                    await conv.send_message(BuildMsg(ID, 'TOO_SLOW_STARTOVER'))
                    del data_cache[ID]
                    return
                try:
                    await UserClient.sign_in(password=DATA['TWO_STEP_VERIFICATION_PASSWORD'])
                except Exception as e:
                    await event.respond(BuildMsg(ID, 'ERROR_REPORT_IT').format(config['HELP_SUPPORT_GROUP'], e))
                    del data_cache[ID]
                    return
        user_client_string_session = UserClient.session.save()
        database.add_created_string_session(ID)
        await event.respond(BuildMsg(ID, 'CREATED_STRING_SESSION').format('telethon', user_client_string_session))

async def generate_pyrogram_string_session(event):
    pass