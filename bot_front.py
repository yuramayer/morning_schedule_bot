import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from os import getenv
from sys import exit
from bot_backend import get_date, no_date, get_day, get_time, to_base

new_dict = {}

#  Run - Edit Configurations - Environment variables
bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit('Error: no token provided')

user_id = int(getenv("USER_ID"))
if not user_id:
    exit('Error: no user id provided')

bot = Bot(token=bot_token)

dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='clear')
async def cmd_clear(message: types.Message):
    """Clearing the cache"""

    if await is_right_date_and_id(message):
        new_dict.clear()
        keyboard = one_but_keyboard('New day')
        await message.answer('Dictionary is cleared', reply_markup=keyboard)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """Checking the cache in dict"""

    if await is_right_date_and_id(message):
        keyboard = one_but_keyboard('New day')
        if not new_dict:
            await message.answer('I\'ve got no cache', reply_markup=keyboard)
        else:
            await message.answer('Type /clear to clear the cache', reply_markup=keyboard)


async def is_right_date_and_id(message):
    """Checking date & id for all the funcs"""

    if await is_right_id(message):
        if await is_new_date(message):
            return True


async def is_right_id(message):
    """Checking the id"""

    verifiable_id = int(message.chat.id)
    if user_id == verifiable_id:
        return True
    else:
        await message.answer('You\'re not user.')


async def is_new_date(message):
    """Checking the date for unique"""

    date = get_date()
    if no_date(date):
        return True
    else:
        await message.answer('We\'ve already added info for today!')


def one_but_keyboard(but_text):
    """Returning keyboard with one button"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text='{}'.format(but_text))
    keyboard.add(button)
    return keyboard


@dp.message_handler(Text(equals='New day'))
async def get_date_day(message: types.Message):
    """Save date & day to dict"""

    if await is_right_date_and_id(message):
        new_dict['date'] = get_date()
        new_dict['day'] = get_day()
        keyboard = one_but_keyboard('New out')
        await message.answer('Date & day: success', reply_markup=keyboard)


@dp.message_handler(Text(equals='New out'))
async def get_out(message: types.Message):
    """Save out-time to dict"""

    if await is_right_date_and_id(message):
        new_dict['out'] = get_time()
        keyboard = one_but_keyboard('New bus')
        await message.answer('Out: success', reply_markup=keyboard)


@dp.message_handler(Text(equals='New bus'))
async def get_bus(message: types.Message):
    """Save bus-time to dict"""

    if await is_right_date_and_id(message):
        new_dict['bus'] = get_time()
        keyboard = one_but_keyboard('New sub')
        await message.answer('Bus: success', reply_markup=keyboard)


@dp.message_handler(Text(equals='New sub'))
async def get_sub(message: types.Message):
    """Save sub-time to dict"""

    if await is_right_date_and_id(message):
        new_dict['sub'] = get_time()
        keyboard = one_but_keyboard('New school')
        await message.answer('Sub: success', reply_markup=keyboard)


@dp.message_handler(Text(equals='New school'))
async def get_school(message: types.Message):
    """Save school-time to dict"""

    if await is_right_date_and_id(message):
        new_dict['school'] = get_time()
        keyboard = one_but_keyboard('Confirm')
        keyboard.one_time_keyboard = True
        await message.answer('School: success', reply_markup=keyboard)


@dp.message_handler(Text(equals='Confirm'))
async def confirm(message: types.Message):
    """Confirm all the data to the database"""

    if await is_right_date_and_id(message):
        to_base(new_dict)
        new_dict.clear()
        await message.answer('Done')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
