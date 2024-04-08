import asyncio
import logging

from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "z",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    plugins={"root": "Plugins"}
)

logging.basicConfig(level=logging.INFO)

async def main():
    await app.start()
    print(app.me)
    await idle()
    await app.stop()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(main())