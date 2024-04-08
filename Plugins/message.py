from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from fragment import FragmentAPI

from config import FULL_INFO, WELCOME_TEXT

@Client.on_message(filters.text)
async def on_msg(c: Client, m: Message):
    if m.text.startswith("/start"):
        return await m.reply(
            WELCOME_TEXT.format(c.me.username),
            quote=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Try it now", switch_inline_query_current_chat="")
                    ]
                ]
            )
        )
    elif m.text.startswith("nft "):
        query = m.text.split()[1].strip().replace("@", "")
        api = FragmentAPI()
        async with api:
            usernames = await api.usernames.search(query)
            if not usernames:
                return await m.reply("No results, try with another username :D", quote=True)
            else:
                username = usernames[0]
                if username.get("status") == "taken":
                    return await m.reply(f"- This username @{username.get('username')} is not available in fragment.com")
                info = await api.usernames.info(username.get("username"))
                address = "`"+info.get("ownership_history")[0].get("buyer")+"`" if info.get("ownership_history") else "[More info here](https://fragment.com/username/{})".format(info.get("username"))
                text = FULL_INFO.format(
                    username=info.get("username"),
                    address=address,
                    status=info.get("status"),
                    ton=username.get("value"),
                    me=c.me.username
                )
                if info.get("ownership_history"):
                        reply_markup = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("View Collectibles", "uwu")
                                ]
                            ]
                        )
                        balance_req = await api._session.request(
                            "get",
                            "https://toncenter.com/api/v3/wallet?address={}".format(info.get("ownership_history")[0].get("buyer"))
                        )
                        balance = (await balance_req.json()).get("balance")
                        reply_markup.inline_keyboard.append(
                            [
                                InlineKeyboardButton("Owner Balance : {:.9f} TON".format(int(balance) / 1000000000), "None")
                            ]
                        )
                else:
                        reply_markup = InlineKeyboardMarkup([])
                reply_markup.inline_keyboard.append(
                        [
                            InlineKeyboardButton("Python Projects 🐍", url="https://t.me/Y88F8")
                        ]
                    )
                return await m.reply(
                    text,
                    quote=True,
                    reply_markup=reply_markup
                )