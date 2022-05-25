#!/opt/homebrew/bin/python3

import asyncio
import telegram

TOKEN = "5336934102:AAEmTN_9-Z12RH3tMbXjasRgKYq0CNGQjo8"
CHAT = "-1001540276501"

async def main():
    bot = telegram.Bot(TOKEN)
    async with bot:
        await bot.send_message(text='VALTÃO TIGRÃO!', chat_id=CHAT)

if __name__ == '__main__':
    asyncio.run(main())
