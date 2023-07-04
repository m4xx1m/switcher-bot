import asyncio
import os

import aiogram


# https://github.com/KeyZenD/modules/blob/138dd06d80a22f7fa7c276c7c5c7319209510ee3/Switcher.py#L41
RU = """ёйцукенгшщзхъфывапролджэячсмитьбю.Ё"№;%:?ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"""
EN = """`qwertyuiop[]asdfghjkl;'zxcvbnm,./~@#$%^&QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>?"""


async def handle(callback: aiogram.types.InlineQuery):
    if not (text := callback.query):
        return

    text = str.translate(text, str.maketrans(RU+EN, EN+RU))

    await callback.answer(
        results=[aiogram.types.InlineQueryResultArticle(
            id=str(hash(text)),
            title=text,
            input_message_content=aiogram.types.InputTextMessageContent(message_text=text, parse_mode=None)
        )]
    )


async def main():
    if (token := os.getenv("BOT_TOKEN", None)) is None:
        raise ValueError("Invalid BOT_TOKEN")

    bot = aiogram.Bot(token=token)
    dispatcher = aiogram.Dispatcher()
    dispatcher.inline_query.register(callback=handle)

    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
