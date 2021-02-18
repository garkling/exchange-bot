import logging
from aiogram import Bot, Dispatcher, types, executor

import exceptions
import config
import messages
from exchanger import Exchanger

logging.basicConfig(level=logging.INFO)
bot = Bot(config.BOT_TOKEN)
disp = Dispatcher(bot)
exchanger = Exchanger()


@disp.message_handler(commands=['start', 'help'])
async def help_command(message: types.Message):
    await message.answer(messages.HELP_TEXT, parse_mode='markdown')


@disp.message_handler(commands=['list', 'lst'])
async def show_currencies_list_command(message: types.Message):
    text = exchanger.get_currency_list()
    await message.answer(f'<code>{text}</code>', parse_mode='html')


@disp.message_handler(commands=['exchange'], regexp=r' (\W+)?([0-9.]+)(\S+)? ([A-Z]{3})?\s?to ([A-Z]{3})')
async def exchange_command(message: types.Message, regexp):
    try:
        conv = exchanger.convert(regexp.groups())
    except (exceptions.InvalidInputError, ValueError):
        answer = 'Please, enter valid message in format \n' \
                    '[symbol][amount] or [amount] [currency] to [currency]'
        await message.answer(answer)
        return

    answer = f'*{conv.from_} -> {conv.to}*\n' \
             f'{[str(conv.value) + conv.sym, conv.sym + str(conv.value)][conv.prefix]}'
    await message.answer(answer, parse_mode='markdown')


@disp.message_handler(commands=['history'], regexp=r' ([A-Z]{3})/([A-Z]{3}) for (\d+) days')
async def show_history_command(message: types.Message, regexp):
    try:
        buffer = exchanger.get_history_chart_image(regexp.groups())
    except (exceptions.InvalidInputError, ValueError):
        answer = 'Please, enter valid message in format \n' \
                    '[currency]/[currency] for [n] days'
        await message.answer(answer)
        return

    await message.answer_photo(buffer, caption='History graph')


@disp.message_handler()
async def handle_plain_text(message: types.Message):
    answer = 'Invalid command format. Try /help for info'
    await message.answer(answer)


if __name__ == '__main__':
    executor.start_polling(disp, skip_updates=True)
