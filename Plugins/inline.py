from pyrogram import Client, enums
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from fragment import FragmentAPI

from config import FULL_INFO, WELCOME_TEXT

@Client.on_inline_query()
async def search_inline(c: Client, inline: InlineQuery):
    if not inline.query:
        return await inline.answer(
            results=[
                InlineQueryResultArticle(
                    title="Welcome to fragment.com bot",
                    description="Type username to search in fragment",
                    url="https://fragment.com/",
                    thumb_url="https://i.ibb.co/2ZZkNMp/photo-2024-04-05-20-39-59.jpg",
                    input_message_content=InputTextMessageContent(
                        message_text=WELCOME_TEXT.format(c.me.username),
                        parse_mode=enums.ParseMode.MARKDOWN
                    )
                )
            ],
            cache_time=60,
            switch_pm_parameter="help",
            switch_pm_text="How to use ?"
        )
    else:
        results = []
        query = inline.query.strip().replace("@", "")
        api = FragmentAPI()
        async with api:
            usernames = await api.usernames.search(query)
            if not usernames:
                return await inline.answer(
                    results=[
                        InlineQueryResultArticle(
                            title="No results",
                            description="Try again with another username",
                            thumb_url="https://em-content.zobj.net/source/apple/391/warning_26a0-fe0f.png",
                            input_message_content=InputTextMessageContent(
                                message_text=WELCOME_TEXT.format(c.me.username),
                                parse_mode=enums.ParseMode.MARKDOWN
                            )
                        )
                    ],
                    switch_pm_parameter="help",
                    switch_pm_text="How to use ?"
                )
            for username in usernames[:15]:
                if username.get("status") == "taken":
                    results.append(
                        InlineQueryResultArticle(
                            title="@"+username.get("username"),
                            description="Not available in fragment.com",
                            input_message_content=InputTextMessageContent(
                                message_text=f"- This username @{username.get('username')} is not available in fragment.com",
                                disable_web_page_preview=True
                            ),
                            thumb_url="https://i.ibb.co/XJhzWt9/no.jpg",
                            thumb_height=128,
                            thumb_width=128
                        )
                    )
                else:
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
                                    InlineKeyboardButton("View Collectibles", url="https://tonviewer.com/{}?section=nfts".format(info.get("ownership_history")[0].get("buyer")))
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
                    results.append(
                        InlineQueryResultArticle(
                            title="@"+info.get("username") + " {} TON".format(username.get("value")),
                            description=info.get("status") + " - fragment.com",
                            thumb_url="https://nft.fragment.com/username/{}.webp".format(info.get("username")),
                            input_message_content=InputTextMessageContent(
                                text,
                                disable_web_page_preview=False
                            ),
                            reply_markup=reply_markup
                        )
                    )
            return await inline.answer(
                results=results,
                cache_time=60,
                switch_pm_parameter="help",
                switch_pm_text="How to use ?"
            )