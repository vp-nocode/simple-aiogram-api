from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import requests
import keyboards as kb

from config import TOKEN, RAPIDAPI_KEY

class Form(StatesGroup):
   language = State()
   sign = State()

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_horoscope(z_sign):

   # url = "https://best-daily-astrology-and-horoscope-api.p.rapidapi.com/api/Detailed-Horoscope/"
   # querystring = {"zodiacSign":f"{zsign}"}
   # headers = {
   #     "x-rapidapi-key": RAPIDAPI_KEY,
   #     "x-rapidapi-host": "best-daily-astrology-and-horoscope-api.p.rapidapi.com"
   # }
   # response = requests.get(url, headers=headers, params=querystring)
   # print(response.json())
   # return response.json()

   url = f"https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign={z_sign}&day=TODAY"
   response = requests.get(url)
   print(response.json())
   return response.json()

def translate_horoscope(info, dest):
   url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"

   payload = {
      "q": f"{info}",
      "source": "en",
      "target": f"{dest}"
   }
   headers = {
      "x-rapidapi-key": RAPIDAPI_KEY,
      "x-rapidapi-host": "deep-translate1.p.rapidapi.com",
      "Content-Type": "application/json"
   }

   response = requests.post(url, json=payload, headers=headers)
   print(response.json())

   if response.status_code == 200:
      return response.json()
   else:
      return None

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
   await message.answer(text='Select language!', reply_markup=kb.main_kb)
   await state.set_state(Form.language)

@dp.message(Form.language)
async def name(message: Message, state: FSMContext):
   if message.text in kb.zodiac_sign.keys():
      await state.update_data(language=message.text)
   else:
      await state.update_data(language='English')
   user_data = await state.get_data()
   if user_data['language'] in kb.zodiac_sign.keys():
      button_set = kb.zodiac_sign[user_data['language']]
   else:
      button_set = kb.zodiac_sign['English']

   await message.answer("Choose your zodiac sign!", reply_markup=await kb.kb_dynamic(button_set))
   await state.set_state(Form.sign)

@dp.message(Form.sign)
async def name(message: Message, state: FSMContext):
   await state.update_data(sign=message.text)
   user_data = await state.get_data()
   info = 'No horoscope for you'

   zodiac_set = kb.zodiac_sign[user_data['language']]
   if user_data['sign'] in zodiac_set:
      ind = zodiac_set.index(user_data['sign'])
      z_sign = kb.zodiac_sign['English'][ind].lower()
      day_horoscope = get_horoscope(z_sign)
      if day_horoscope['success']:
         info = f"Prediction for {day_horoscope['data']['date']}: {day_horoscope['data']['horoscope_data']}"
      if user_data['language'] != 'English':
         translate_info = translate_horoscope(info, kb.lang_set[user_data['language']])
         if translate_info is not None:
            info = translate_info['data']['translations']['translatedText']
         print(info)
   await message.answer(info)

async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())
