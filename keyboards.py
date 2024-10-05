from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


zodiac_sign = {'English': ['Aries','Leo','Sagittarius','Taurus','Virgo','Capricorn','Gemini','Libra','Aquarius','Cancer','Scorpio','Pisces'],
         'Russian': ['Овен','Лев','Стрелец', 'Телец','Дева','Козерог','Близнецы','Весы','Водолей','Рак','Скорпион','Рыбы'],
         'Greek':['Κριός','Λέον','Τοξότης','Ταύρος','Παρθένος','Αιγόκερως','Δίδυμος','Ζυγός','Υδροχόος','Καρκίνος','Σκορπιός','Ιχθείς']}

lang_set = {'Russian': 'ru', 'Greek':'el'}

main_kb = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="English"), KeyboardButton(text="Greek"), KeyboardButton(text="Russian") ]
], resize_keyboard=True)

async def kb_dynamic(button_set):
   keyboard = ReplyKeyboardBuilder()
   for key in button_set:
      button = KeyboardButton(text=key)
      keyboard.add(button)
   return keyboard.adjust(3).as_markup(resize_keyboard=True)
