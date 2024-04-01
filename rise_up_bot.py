from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

token = '6614357547:AAE34YQfsHz1EFTS6y0S6gGNAFHM9ZOiDB4'

respond_cb = CallbackData('respond', 'chat_id', 'text', 'action')


class Admin(StatesGroup):
    answer = State()


class Question(StatesGroup):
    user = State()
    admin = State()


bot = Bot(token=token)

storage = MemoryStorage()

dp = Dispatcher(bot=bot, storage=storage)


def get_markup(user_id, message):
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='Javob berish',
                             callback_data=respond_cb.new(chat_id=user_id, text=message, action='text')))
    return markup


async def on_startup(_):
    await bot.send_message(chat_id=1329197690,
                           text='Bot ishga tushdi')
    print('Bot ishga tushdi')


@dp.message_handler(commands=['start'])
async def cm_start(message: types.Message):
    await message.reply(
        text=f"Salom {message.from_user.full_name}\nBu bot orqali savollaringizni ustozga murojat qilishingiz mumkin")


@dp.message_handler(commands=['info'])
async def cm_info(message: types.Message):
    mes = f'''
/start - botni ishga tushirish
/info - bot malumotlarini olsih
/help - yoram olish
/savol - ustoz bilan aloqa'''
    await message.reply(text=mes)


@dp.message_handler(commands=['help'])
async def cm_help(message: types.Message):
    mes = f"""
But bot orqali szi to'g'ridan to'g'ri uztoz bilan aloqa ornatsiz!"""
    await message.reply(text=mes)


@dp.message_handler(commands=['savol'])
async def cm_savol(message: types.Message):
    await message.answer(text="Savolingizni matin ko'rinishida yuboring!")
    await Question.user.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=Question.user)
async def user_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await message.answer(text='Savolingiz ustozga yuborildi tez orada aloqaga chiqiladi')
    await bot.send_message(chat_id=1329197690,
                           text=message.text,
                           reply_markup=get_markup(message.from_user.id, message.text))
    await state.finish()


@dp.callback_query_handler(respond_cb.filter(action='text'), chat_id=1329197690)
async def check_admin(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=f"Savol -- {callback_data['text']}\n\nJavobingizni yo'llang")
    await Question.admin.set()
    async with state.proxy() as data:
        data['text'] = callback_data['text']
        data['chat_id'] = callback_data['chat_id']


@dp.message_handler(state=Question.admin, chat_id=1329197690)
async def answer_admin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        text = data['text']
        chat_id = data['chat_id']
    mes = f"""
student - {text}\n
teacher - {message.text}"""
    await bot.send_message(chat_id=chat_id, text=mes)
    await state.finish()


@dp.message_handler(content_types=types.ContentType.TEXT)
async def send_text(message: types.Message):
    await bot.forward_message(chat_id=1329197690, from_chat_id=message.chat.id, message_id=message.message_id,
                              message_thread_id=message.message_thread_id)


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def send_photo(message: types.Message):
    await bot.forward_message(chat_id=1329197690, from_chat_id=message.chat.id, message_id=message.message_id,
                              message_thread_id=message.message_thread_id)


@dp.message_handler(content_types=types.ContentType.VOICE)
async def send_voice(message: types.Message):
    await bot.forward_message(chat_id=1329197690, from_chat_id=message.chat.id, message_id=message.message_id,
                              message_thread_id=message.message_thread_id)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
