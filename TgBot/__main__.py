from TgBot import bot, BOT_TOKEN

def main():
    bot.start(bot_token=BOT_TOKEN)
    print('Bot has been started!')
    bot.run_until_disconnected()

main()