import telebot
from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup
import logging

logging.basicConfig(level='INFO', filename='logs.log')
logger = logging.getLogger()

API_KEY = '5147041361:AAGQM-EGM5J_jZmc2xVVafpsrmNjXUGK830'
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello my dear friend! If you wanna take testing please write command /test')


@bot.message_handler(commands=['test'])
def test_handler(message):
    bot.send_message(message.chat.id, 'What\'s your name?')
    bot.register_next_step_handler(message, select_age)


def select_age(message):
    bot.send_message(message.chat.id, 'Your age?')
    bot.register_next_step_handler(message, select_sex)


def select_sex(message):
    try:
        mkp = InlineKeyboardMarkup()
        mkp.row_width = 3
        mkp.add(InlineKeyboardButton('male', callback_data='male'),
                InlineKeyboardButton('female', callback_data='female'),
                InlineKeyboardButton('other', callback_data='other'))
        bot.send_message(message.chat.id, 'What\'s you sex?', reply_markup=mkp)
    except Exception as err:
        send_error_message(err, message)


@bot.callback_query_handler(func=lambda msg: True)
def callback_query_handler(call):
    try:
        if call.data == 'male' or call.data == 'female':
            bot.send_message(call.message.chat.id, 'Ok, you are good')
            finish(call.message)

        elif call.data == 'other':
            mkp = InlineKeyboardMarkup()
            mkp.row_width = 2
            mkp.add(InlineKeyboardButton('I shure', callback_data='YouShureYes'),
                    InlineKeyboardButton('I not shure', callback_data='YouShureNo'))
            bot.answer_callback_query(call.id, f'Realy {call.data}??))')
            bot.send_message(call.message.chat.id, 'Sex Other? Your shure?', reply_markup=mkp)

        if call.data == 'YouShureYes':
            bot.send_message(call.message.chat.id, 'Ok, you are good')
            finish(call.message)
        elif call.data == 'YouShureNo':
            bot.send_message(call.message.chat.id, 'Ok, try again')
            select_sex(call.message)

        if call.data == 'WannaTestingYes':
            test_handler(call.message)
        elif call.data == 'WannaTestingNo':
            bot.send_message(call.message.chat.id, 'Ok. When you want take the testing please write command /test')
    except Exception as err:
        send_error_message(err, call.message)


def finish(message):
    try:
        mkp = InlineKeyboardMarkup()
        mkp.row_width = 2
        mkp.add(InlineKeyboardButton('Yes', callback_data='WannaTestingYes'),
                InlineKeyboardButton('No', callback_data='WannaTestingNo'))
        bot.send_message(message.chat.id, 'You wanna take  the testing?', reply_markup=mkp)
    except Exception as err:
        send_error_message(err, message)


def send_error_message(error, message):
    logger.critical(error)
    bot.send_message(message.chat.id, 'ooops, something is not working')

if __name__=='__main__':
    print('bot is started')
    bot.infinity_polling()
