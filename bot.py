import os

from aiogram import Bot, Dispatcher, executor, types
import logging

import api

# import set_keys


API_TOKEN = os.environ['BOT_TOKEN']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    await msg.reply("Привет!\nОтправь мне ссылку на статью чтобы получить краткий пересказ.")


@dp.message_handler()
async def send_retell(msg: types.Message):
    url = ''
    for i in msg.entities:
        if i.type == 'text_link':
            url = i.url
            break
        elif i.type == 'url':
            url = msg.text[i.offset:i.offset+i.length]
    link_to_retell = api.get_link_to_retell(url)
    if link_to_retell.get('status') == 'success':
        retell = api.get_retell(link_to_retell.get('sharing_url'))
        title = f'<b>{retell.get("title")}</b>'
        content = '\n\n'.join(retell.get('content'))
        msg_text = f'{title}\n\n{content}\n\nВзято из: {link_to_retell.get("sharing_url")}'
        await msg.reply(msg_text, parse_mode=types.ParseMode.HTML)
    else:
        await msg.reply('Похоже это не ссылка на статью :(')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
