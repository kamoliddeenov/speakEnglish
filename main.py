import logging
from aiogram import Bot, Dispatcher, executor, types

from oxfordLookup import getDefinitions
from googletrans import Translator

translator = Translator()
API_TOKEN = 'TOKEN' # Your bot token here

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply(f"Assalomu alaykum {message.from_user.full_name}. SpeakEnglish botga xush kelibsiz.\nYordam uchun /help buyrug'ini yuboring.")

@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.reply("Men ingliz tilidagi matnlarni o'zbek tiliga, va aksincha o'zbek tilidagi matnlarni ingliz tiliga tarjima qiluvchi botman.\n\nBundan tashqari menga inglizcha so'z yuborib u haqida ma'lumot (definition) olishingiz ham mumkin :)")

@dp.message_handler()
async def tarjimon(message: types.Message):
    lang = translator.detect(message.text).lang
    if len(message.text.split()) > 2:
        dest = 'uz' if lang == 'en' else 'en'
        await message.answer(translator.translate(message.text, dest).text)
    else:
        if lang == 'en':
            word_id = message.text
        else:
            word_id = translator.translate(message.text, dest='en').text
        lookup = getDefinitions(word_id)
        if lookup:
            await message.reply(f"<b>Word:</> {word_id}\n\n<b>Definitions:</>\n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.reply_voice(lookup['audio'])
        else:
            await message.answer("Bunday so'z topilmadi")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)