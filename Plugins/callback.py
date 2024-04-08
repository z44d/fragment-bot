from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from aiohttp import ClientSession

@Client.on_callback_query(filters.regex("^uwu$"))
async def view_nft_items(c: Client, q: CallbackQuery):
    address = q.message.text.split("Owner address : ")[1].split("\n")[0]
    api_url = "https://toncenter.com/api/v3/nft/items?owner_address={}&limit=128&offset=0".format(address)
    async with ClientSession() as session:
        res = await session.request(
            "get",
            url=api_url
        )
        json_res = await res.json()
        if not json_res.get('nft_items'):
            return await q.answer("No Collectibles", show_alert=True)
        usernames = ""
        for i in json_res.get('nft_items'):
            if  i["content"].get("uri") and "/username/" in i["content"]["uri"]:
                f = i["content"]["uri"].split("username/")[1].split(".json")[0]
                usernames += "[@{u}](https://fragment.com/username/{u}) ".format(u=f)
        await q.message.reply_text(
            "All Collectibles:\n\n{}".format(usernames),
            quote=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("View all nft items here", url="https://tonviewer.com/{}?section=nfts".format(address))
                    ]
                ]
            ),
            disable_web_page_preview=True
        )
    return await q.edit_message_reply_markup(
        InlineKeyboardMarkup(
            q.message.reply_markup.inline_keyboard[1:]
        )
    )