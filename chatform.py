#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import ReplyKeyboardMarkup, KeyboardButton,ParseMode,ReplyKeyboardRemove
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
import emoji
import datetime
from dbhelper import DBHelper

db = DBHelper()
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE, LOCATION_CHOICE, DETAIL_CHOICE = range(5)
Lokasi = KeyboardButton(text="Lokasi", request_location=True)

reply_keyboard = [['Agenda', 'Materi','Pembicara'],
                  ['Tanggal', 'Waktu','Tempat'],
                  ['Peta Lokasi','Penyelenggara','Lainnya'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def toEmoji(k,v):
    if k =='Agenda':
       r=emoji.emojize(":books: *{}* :books:".format(v))
    elif k=='Pembicara':
       r=emoji.emojize("\n \n Bersama :\n :man_with_turban: *{}*".format(v),use_aliases=True)
    elif k=='Materi' :
       r=emoji.emojize(":mag: Tema :\n *\"{}\"*".format(v),use_aliases=True)
    elif k=='Tanggal' :
       r=emoji.emojize(":date: {}".format(get_hari(v)),use_aliases=True)
    elif k=='Waktu' :
       r=emoji.emojize(":alarm_clock: {}".format(v),use_aliases=True)
    elif k=='Tempat' :
       r=emoji.emojize(":mosque: {}".format(v),use_aliases=True)
    elif k=='Peta Lokasi' :
       r=emoji.emojize(":pushpin: {}".format(v),use_aliases=True)
    elif k=='Penyelenggara' :
       r=emoji.emojize("\n *Organized by :* \n {}".format(v),use_aliases=True)
    else :
       r="{} {}".format(k,v)
    return r

def emojiFormat(k,v):
    if k =='agenda':
       r=emoji.emojize(":books: *{}* :books:".format(v))
    elif k=='pembicara':
       r=emoji.emojize("\n \n Bersama :\n :man_with_turban: *{}*".format(v),use_aliases=True)
    elif k=='materi' :
       r=emoji.emojize(":mag: Tema :\n *\"{}\"*".format(v),use_aliases=True)
    elif k=='tanggal' :
       r=emoji.emojize(":date: {}".format(date2day(v)),use_aliases=True)
    elif k=='waktu' :
       r=emoji.emojize(":alarm_clock: {}".format(v),use_aliases=True)
    elif k=='lokasi' :
       r=emoji.emojize(":mosque: {}".format(v),use_aliases=True)
    elif k=='latlon' :
       r=emoji.emojize(":pushpin: {}".format(v),use_aliases=True)
    elif k=='host' :
       r=emoji.emojize("\n *Organized by :* \n {}".format(v),use_aliases=True)
    else :
       r="{} {}".format(k,v)
    return r

def tombol(text):
    if text == 'tanggal':
       t="Masukkan Tanggal (DD-MM-YYYY) [mis : 24-05-2019]"
    else :
       t='{} adalah : '.format(text.lower())
    return t

def get_hari(text):
    if text:
       hari = ['Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Ahad']
       tgl = datetime.datetime.strptime(text,'%d-%m-%Y').strftime('%Y-%m-%d')
       wd = datetime.datetime.strptime(tgl,'%Y-%m-%d').weekday()
       return  (hari[wd],tgl)
    else :
       return ''

def date2day(text):
    if text:
       hari = ['Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Ahad']
       tgl = datetime.datetime.strptime(text,'%Y-%m-%d').strftime('%d-%m-%Y')
       wd = datetime.datetime.strptime(tgl,'%d-%m-%Y').weekday()
       return  "{}, {}".format(hari[wd],tgl)
    else :
       return ''


def facts_to_str(user_data):
    #print(user_data)
    facts = list()

    for key, value in user_data.items():
        #facts.append('{} : {}'.format(key, value))
        facts.append(toEmoji(key,value))
    #print(facts)
    return "\n".join(facts).join(['\n', '\n'])

def kajian_text(data):
    #print(data)
    ngaji = list()
    for key,value in data.items():
        if value:
           ngaji.append(emojiFormat(key,value))
        else :
           pass
    #print(ngaji)
    return "\n".join(ngaji).join(['\n', '\n'])

def check_data(key,array):
    if key in array:
       return array[key]
    else :
       return ''

def simpan_data(userid,user_data):
    user_id = userid
    #print(user_data)
    if user_data:
       agenda = check_data('Agenda',user_data)
       materi = check_data('Materi',user_data)
       pembicara = check_data('Pembicara',user_data)
       tanggal = get_hari(check_data('Tanggal',user_data))
       waktu = check_data('Waktu',user_data)
       tempat = check_data('Tempat',user_data)
       latlon = check_data('Peta Lokasi',user_data)
       host = check_data('Penyelenggara',user_data)
       return db.add_info(agenda,pembicara,materi,tempat,tanggal[0],tanggal[1],waktu,host,latlon[0],latlon[1],user_id) 
    else :
      pass

def start(bot, update):
    reply_keyboard = [['Tambah Agenda'],['Lihat Agenda']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    greating = ("Assalamu'alaikum {}! Selamat datang di info ngajimu \n" 
                "Bot ini adalah untuk membuat dan melihat jadwal kajian \n"
                "Untuk menambah agenda silakan pilih *[Tambah Agenda]* \n" 
                "Untuk melihat agenda yang sudah tersimpan pilih *[Lihat Agenda]*".format(update.message.from_user.username))

    update.message.reply_text(greating, parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup)

    return CHOOSING

def info_add(bot,update):
    greating = "Hi {}! Adakah info kajian yang akan diumumkan? \n tambahkan agendamu dengan memilih tombol yang ada".format(update.message.from_user.username)

    update.message.reply_text(greating,
        reply_markup=markup)

    return CHOOSING

def lihat_info(bot,update):
    #print("pilih lihat agenda")
    '''
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard) '''
    buttons = []

    update.message.reply_text("Lihat Agenda dalam sepekan ini :\n")
    #print(update.message.text)
    info = db.get_sepekan()
    if not info: 
       print("tidak ada agenda")
       update.message.reply_text("Belum ada agenda pekan ini")
       pass
    else :
       for i in info:
           buttons.append(
           [InlineKeyboardButton(text= '{}, {}'.format(i[1],i[2]),callback_data= i[0])]
           )
       keyboard = InlineKeyboardMarkup(buttons)
       update.message.reply_text('Berikut Agendanya: ',reply_markup = keyboard)
    return DETAIL_CHOICE

def detail(bot,update):
    query = update.callback_query
    detail = db.get_detail(query.data)
    latlon=detail['latlon'].split(',')
    #print(latlon)
    #query.edit_message_text(text="Kajian : {}".format(detail))
    query.message.reply_text(text ="Kajian : {}"
                                    "*Siapkan INFAQ terbaik Anda!* ".format(kajian_text(detail)), parse_mode=ParseMode.MARKDOWN,reply_markup=markup)
    bot.send_location(chat_id=query.message.chat_id,latitude=latlon[0] ,longitude=latlon[1])
    return DETAIL_CHOICE

def regular_choice(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    update.message.reply_text(tombol(text.lower()))

    return TYPING_REPLY

def location_choice(bot,update,user_data):
    text = update.message.text
    user_data['choice'] = text
    update.message.reply_text('Share peta lokasi kegiatan anda!')
    return LOCATION_CHOICE
 
def custom_choice(bot, update):
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')

    return TYPING_CHOICE


def received_information(bot, update, user_data):
    #print(user_data)
    if update.message.location:
       text = (update.message.location.latitude,update.message.location.longitude)
    else :
       text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    #print(facts_to_str(user_data))
    update.message.reply_text("Berikut adalah draft agenda yang sudah anda buat:"
                              "{}"
                              "Anda dapat menambahkan hal lain ataupun mengubah data yang ada.".format(
                                  facts_to_str(user_data)), parse_mode=ParseMode.MARKDOWN,reply_markup=markup)

    return CHOOSING


def done(bot, update, user_data):
    user=update.message.from_user
    userid=user.id
    username = user.first_name
    if 'choice' in user_data:
        del user_data['choice']
    #print(facts_to_str(user_data))
    update.message.reply_text("KUNJUNGILAH!"
                              "{}"
                               ""
                              "*Siapkan Infaq Terbaik Anda!*".format(facts_to_str(user_data)),parse_mode=ParseMode.MARKDOWN)
    simpan_data(userid,user_data) 
    update.message.reply_text("Info kajianmu udah disimpan, terima kasih {}".format(username))

    #update.message.reply_text("Info kajianmu gagal disimpan, mohon diulang lagi /start terima kasih {}".format(username))
    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("600359159:AAEySTHVWGkKRdpnLM2uO7iMS2jdCtg7WfY")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    #db setup
    #db = DBHelper()
    #db.setup()

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^(Agenda|Materi|Pembicara|Tanggal|Waktu|Tempat|Penyelenggara)$',
                                    regular_choice,
                                    pass_user_data=True), 
                       RegexHandler('^Peta Lokasi$',
                                    location_choice,
                                    pass_user_data=True),
                       RegexHandler('^Lainnya$',
                                    custom_choice),
                       RegexHandler('^Lihat Agenda$',
                                    lihat_info),
                       RegexHandler('^Tambah Agenda$',
                                    info_add),
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice,
                                           pass_user_data=True),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
            LOCATION_CHOICE: [MessageHandler(Filters.location,
                                            received_information,
                                            pass_user_data=True)
                            ],
            DETAIL_CHOICE:[CallbackQueryHandler(detail),CommandHandler('start',start)],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)
    #detail_handler = CallbackQueryHandler(button)
    #dp.add_handler(detail_handler)
    #updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    #db = DBHelper()
    db.setup()
    main()
