from config import api_token
from aiogram import Bot, Dispatcher, executor, types

user_state = None
bot = Bot(token=api_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(message.chat.id)
    await message.reply("""
Hi!
I'm wildberries notify bot.

Choose command here or click to menu button in keyboard

Available commands:
/get_cards_ids - Get ids of all cards
/get_cards_links - Get links of all cards
/add_card - Add card
/delete_card - Delete card
/get_timeout - Get timeout (in minutes)
/get_stars_count - Get stars count
/set_timeout - Set timeout (in minutes)
/set_stars_count - Set stars count
""")


@dp.message_handler(commands=['get_timeout'])
async def send_timeout(message: types.Message):
    with open('timeout.txt', 'r') as file:
        timeout = file.read()
        await message.reply(timeout + '\n(in minutes)')


@dp.message_handler(commands=['set_timeout'])
async def set_timeout(message: types.Message):
    global user_state
    user_state = 'set_timeout'
    await message.reply('Send timeout (in minutes)')


@dp.message_handler(commands=['get_stars_count'])
async def send_stars_count(message: types.Message):
    with open('stars_count.txt', 'r') as file:
        stars_count = file.read()
        await message.reply(stars_count)


@dp.message_handler(commands=['set_stars_count'])
async def set_stars_count(message: types.Message):
    global user_state
    user_state = 'set_stars_count'
    await message.reply('Send stars count (only 1, 2, 3, 4 or 5)')


@dp.message_handler(commands=['get_cards_ids'])
async def send_cards_ids(message: types.Message):
    with open('cards.txt', 'r') as file:
        cards_ids = file.read().split()
        await message.reply(' '.join(cards_ids))


@dp.message_handler(commands=['get_cards_links'])
async def send_cards_links(message: types.Message):
    with open('cards.txt', 'r') as file:
        cards_ids = file.read().split()
        answer = []
        for card_id in cards_ids:
            answer.append('https://www.wildberries.ru/catalog/' + card_id + '/feedbacks')
        await message.reply('\n'.join(answer))


@dp.message_handler(commands=['add_card'])
async def add_card(message: types.Message):
    global user_state
    user_state = 'add_card'
    await message.reply('Send link or id of card')


@dp.message_handler(commands=['delete_card'])
async def delete_card(message: types.Message):
    global user_state
    user_state = 'delete_card'
    await message.reply('Send link or id of card')


@dp.message_handler()
async def handle_messages(message: types.Message):
    global user_state

    if user_state == 'add_card':
        is_valid = False
        if message.text.isdigit():
            with open('cards.txt', 'a') as file:
                file.write(message.text + '\n')
            is_valid = True
        else:
            if '/catalog/' in message.text:
                if '/' in message.text[message.text.find('/catalog/') + 9:]:
                    if message.text[message.text.find('/catalog/') + 9:message.text.rfind('/')].isdigit():
                        with open('cards.txt', 'a') as file:
                            file.write(message.text[message.text.find('/catalog/') + 9:message.text.rfind('/')] + '\n')
                        is_valid = True
        if is_valid:
            await message.reply('Card added')
        else:
            await message.reply('Incorrect link or id of card!')
    elif user_state == 'delete_card':
        is_valid = False
        if message.text.isdigit():
            with open('cards.txt', 'r') as file:
                cards_ids = file.read().split()
            with open('cards.txt', 'w') as file:
                if message.text in cards_ids:
                    cards_ids.remove(message.text)
                    file.write('\n'.join(cards_ids) + '\n')
            is_valid = True
        else:
            if '/catalog/' in message.text:
                if '/' in message.text[message.text.find('/catalog/') + 9:]:
                    if message.text[message.text.find('/catalog/') + 9:message.text.rfind('/')].isdigit():
                        with open('cards.txt', 'r') as file:
                            cards_ids = file.read().split()
                        with open('cards.txt', 'w') as file:
                            if message.text[message.text.find('/catalog/') + 9:message.text.rfind('/')] in cards_ids:
                                cards_ids.remove(message.text[message.text.find('/catalog/') + 9:message.text.rfind('/')])
                                file.write('\n'.join(cards_ids) + '\n')
                        is_valid = True
        if is_valid:
            await message.reply('Card deleted')
        else:
            await message.reply('Incorrect link or id of card!')
    elif user_state == 'set_timeout':
        is_valid = False
        if message.text.isdigit():
            is_valid = True
            with open('timeout.txt', 'w') as file:
                file.write(message.text)

        if is_valid:
            await message.reply('Timeout set upped')
        else:
            await message.reply('Incorrect timeout!')
    elif user_state == 'set_stars_count':
        is_valid = False
        if message.text in ['1', '2', '3', '4', '5']:
            is_valid = True
            with open('stars_count.txt', 'w') as file:
                file.write(message.text)

        if is_valid:
            await message.reply('Stars count set upped')
        else:
            await message.reply('Incorrect stars count!')

    user_state = None


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
