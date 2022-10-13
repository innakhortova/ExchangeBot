import requests
import sqlite3
from bs4 import BeautifulSoup as b
import emoji
import telebot
from telebot import types
from random import choice

URL = "https://myfin.by/currency/mogilev"
URL2 = "https://www.finversia.ru/finhandbook/aphorisms"
HEADERS = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0'
}
TOKEN = '5407612264:AAFrU6CvQ-HVbwwG6U7jZlXgQZU0VZoak48'
bot = telebot.TeleBot(TOKEN)

r = requests.get(URL, headers=HEADERS)

soup = b(r.text, 'html.parser')
table1 = soup.find('table', id='currency-table')
tm = soup.find('div', class_='c-torgi__date')
time = tm.text
lst = []
for i in table1.find_all("td"):
    title = i.text
    lst.append(title)


r2 = requests.get(URL2, headers=HEADERS)
soup = b(r2.text, "html.parser")
all_facts = soup.find_all("div", class_="b-quote")
clear_facts = [i.text for i in all_facts]
fact = choice(clear_facts).replace("\n", " ")

bank1 = lst.index('Паритетбанк')
ParitetBank = lst[bank1:(bank1 + 7)]
bank2 = lst.index('Альфа-Банк')
AlfaBank = lst[bank2:(bank2 + 7)]
bank3 = lst.index('Банк БелВЭБ')
BelVebBank = lst[bank3:(bank3 + 7)]
bank4 = lst.index('Банк ВТБ (Беларусь)')
VtbBank = lst[bank4:(bank4 + 7)]
bank5 = lst.index('Белагропромбанк')
BelagropromBank = lst[bank5:(bank5 + 7)]
bank6 = lst.index('Беларусбанк')
BelarusBank = lst[bank6:(bank6 + 7)]
bank7 = lst.index('Белгазпромбанк')
BelgaspromBank = lst[bank7:(bank7 + 7)]
bank8 = lst.index('Белинвестбанк')
BelinvestBank = lst[bank8:(bank8 + 7)]
bank9 = lst.index('БНБ-Банк')
BnbBank = lst[bank9:(bank9 + 7)]
bank10 = lst.index('БТА Банк')
BtaBank = lst[bank10:(bank10 + 7)]
bank11 = lst.index('МТБанк')
MtBank = lst[bank11:(bank11 + 7)]
bank12 = lst.index('Приорбанк')
PriorBank = lst[bank12:(bank12 + 7)]
bank13 = lst.index('РРБ-Банк')
RrbBank = lst[bank13:(bank13 + 7)]
bank14 = lst.index('Сбер Банк')
SberBank = lst[bank14:(bank14 + 7)]
bank15 = lst.index('Технобанк')
TehnoBank = lst[bank15:(bank15 + 7)]

res_pars = [ParitetBank, AlfaBank, BelVebBank, VtbBank, BelagropromBank, BelarusBank, BelgaspromBank, BelinvestBank,
            BnbBank, BtaBank, MtBank, PriorBank, RrbBank, SberBank, TehnoBank]
print(res_pars)

with sqlite3.connect('bank_db.db') as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS request (bank TEXT, usd_buy TEXT, usd_sell TEXT,
    eur_buy TEXT, eur_sell TEXT, rub_buy TEXT, rub_sell TEXT)""")
    cur.executemany("""INSERT INTO request (bank, usd_buy, usd_sell, eur_buy, eur_sell, rub_buy, rub_sell)
            VALUES(?,?,?,?,?,?,?)""", res_pars)
    cur.execute("""DELETE from request where rowid IN (Select rowid from request limit 15)""")
    usd_all = cur.execute("""SELECT bank, usd_buy, usd_sell FROM request ORDER BY usd_buy DESC""").fetchall()
    eur_all = cur.execute("""SELECT bank, eur_buy, eur_sell FROM request ORDER BY eur_buy DESC""").fetchall()
    rub_all = cur.execute("""SELECT bank, rub_buy, rub_sell FROM request ORDER BY rub_buy DESC""").fetchall()
    best_usd_buy = cur.execute("""SELECT bank, usd_buy FROM request ORDER BY usd_buy DESC""").fetchall()
    best_usd_sell = cur.execute("""SELECT bank, usd_sell FROM request ORDER BY usd_sell ASC""").fetchall()
    best_eur_buy = cur.execute("""SELECT bank, eur_buy FROM request ORDER BY eur_buy DESC""").fetchall()
    best_eur_sell = cur.execute("""SELECT bank, eur_sell FROM request ORDER BY eur_sell ASC""").fetchall()
    best_rub_buy = cur.execute("""SELECT bank, rub_buy FROM request ORDER BY rub_buy DESC""").fetchall()
    best_rub_sell = cur.execute("""SELECT bank, rub_sell FROM request ORDER BY rub_sell ASC""").fetchall()

res_usd_buy = [' : '.join(i) for i in best_usd_buy]
res_usd_sell = [' : '.join(i) for i in best_usd_sell]
res_eur_buy = [' : '.join(i) for i in best_eur_buy]
res_eur_sell = [' : '.join(i) for i in best_eur_sell]
res_rub_buy = [' : '.join(i) for i in best_rub_buy]
res_rub_sell = [' : '.join(i) for i in best_rub_sell]

print(res_usd_buy)
@bot.message_handler(commands=['start', 'help'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=emoji.emojize("USD :dollar_banknote:"), callback_data='usd')
    btn2 = types.InlineKeyboardButton(text=emoji.emojize("EUR :euro_banknote:"), callback_data='eur')
    btn3 = types.InlineKeyboardButton(text=emoji.emojize("RUB :Russia:"), callback_data='rub')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text=emoji.emojize(f'Привет, <b>{message.from_user.first_name}</b>! '
                                      f':person_raising_hand: \n  Я виртуальный помощник. С удовольствием подскажу '
                                      f'лучший курс обмена :money_with_wings: и покупки валюты :money_bag:, '
                                      f'а также банк :bank:, в котором ты сможешь совершить данную операцию. \n  '
                                      f' Для начала выбери интересующую тебя валюту... \n Последнее обновление: \n'
                                      f' <b>{time}</b>'), parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'usd':
        markupusd = types.InlineKeyboardMarkup()
        btnusdbuy = types.InlineKeyboardButton(text=emoji.emojize("Обменять :dollar_banknote:"), callback_data='usd_buy')
        btnusdsell = types.InlineKeyboardButton(text=emoji.emojize("Купить :dollar_banknote:"), callback_data='usd_sell')
        markupusd.add(btnusdbuy, btnusdsell)
        bot.send_message(call.message.chat.id, text=emoji.emojize("Тебя интересует покупка или обмен? Пожалуйста, "
                                                    "сделай свой выбор! :person_shrugging:"), reply_markup=markupusd)
    if call.data == 'eur':
        markupeur = types.InlineKeyboardMarkup()
        btneurbuy = types.InlineKeyboardButton(text=emoji.emojize("Обменять :euro_banknote:"), callback_data='eur_buy')
        btneursell = types.InlineKeyboardButton(text=emoji.emojize("Купить :euro_banknote:"), callback_data='eur_sell')
        markupeur.add(btneurbuy, btneursell)
        bot.send_message(call.message.chat.id, text=emoji.emojize("Тебя интересует покупка или обмен? Пожалуйста,"
                                                    " сделай свой выбор! :person_shrugging:"), reply_markup=markupeur)
    if call.data == 'rub':
        markuprub = types.InlineKeyboardMarkup()
        btnrubbuy = types.InlineKeyboardButton(text=emoji.emojize("Обменять :Russia:"), callback_data='rub_buy')
        btnrubsell = types.InlineKeyboardButton(text=emoji.emojize("Купить :Russia:"), callback_data='rub_sell')
        markuprub.add(btnrubbuy, btnrubsell)
        bot.send_message(call.message.chat.id, text=emoji.emojize("Тебя интересует покупка или обмен? Пожалуйста, "
                                                    "сделай свой выбор! :person_shrugging:"), reply_markup=markuprub)
    if call.data == 'usd_buy':
        photo = open('img/dollar1.png', 'rb')
        bot.send_photo(call.message.chat.id, photo)
        fact = choice(clear_facts).replace("\n", " ")
        bot.send_message(call.message.chat.id, text=fact)
        bot.send_message(call.message.chat.id, '\n'.join(map(str, res_usd_buy)))
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text=emoji.emojize("USD :dollar_banknote:"), callback_data='usd')
        btn2 = types.InlineKeyboardButton(text=emoji.emojize("EUR :euro_banknote:"), callback_data='eur')
        btn3 = types.InlineKeyboardButton(text=emoji.emojize("RUB :Russia:"), callback_data='rub')
        markup.add(btn1, btn2, btn3)
        bot.send_message(call.message.chat.id, text=emoji.emojize(':money-mouth_face:')*9, reply_markup=markup)
    if call.data == 'usd_sell':
        photo = open('img/dollar2.jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo)
        fact = choice(clear_facts).replace("\n", " ")
        bot.send_message(call.message.chat.id, text=fact)
        bot.send_message(call.message.chat.id, '\n'.join(map(str, res_usd_sell)))
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text=emoji.emojize("USD :dollar_banknote:"), callback_data='usd')
        btn2 = types.InlineKeyboardButton(text=emoji.emojize("EUR :euro_banknote:"), callback_data='eur')
        btn3 = types.InlineKeyboardButton(text=emoji.emojize("RUB :Russia:"), callback_data='rub')
        markup.add(btn1, btn2, btn3)
        bot.send_message(call.message.chat.id, text=emoji.emojize(':money-mouth_face:')*9, reply_markup=markup)
    if call.data == 'eur_buy':
        photo = open('img/euro.jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo)
        fact = choice(clear_facts).replace("\n", " ")
        bot.send_message(call.message.chat.id, text=fact)
        bot.send_message(call.message.chat.id, '\n'.join(map(str, res_eur_buy)))
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text=emoji.emojize("USD :dollar_banknote:"), callback_data='usd')
        btn2 = types.InlineKeyboardButton(text=emoji.emojize("EUR :euro_banknote:"), callback_data='eur')
        btn3 = types.InlineKeyboardButton(text=emoji.emojize("RUB :Russia:"), callback_data='rub')
        markup.add(btn1, btn2, btn3)
        bot.send_message(call.message.chat.id, text=emoji.emojize(':money-mouth_face:')*9, reply_markup=markup)
    if call.data == 'eur_sell':
        photo = open('img/euro1.jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo)
        fact = choice(clear_facts).replace("\n", " ")
        bot.send_message(call.message.chat.id, text=fact)
        bot.send_message(call.message.chat.id, '\n'.join(map(str, res_eur_sell)))
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text=emoji.emojize("USD :dollar_banknote:"), callback_data='usd')
        btn2 = types.InlineKeyboardButton(text=emoji.emojize("EUR :euro_banknote:"), callback_data='eur')
        btn3 = types.InlineKeyboardButton(text=emoji.emojize("RUB :Russia:"), callback_data='rub')
        markup.add(btn1, btn2, btn3)
        bot.send_message(call.message.chat.id, text=emoji.emojize(':money-mouth_face:')*9, reply_markup=markup)
    if call.data == 'rub_buy':
        photo = open('img/100rub2jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo)
        fact = choice(clear_facts).replace("\n", " ")
        bot.send_message(call.message.chat.id, text=fact)
        bot.send_message(call.message.chat.id, '\n'.join(map(str, res_rub_buy)))
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text=emoji.emojize("USD :dollar_banknote:"), callback_data='usd')
        btn2 = types.InlineKeyboardButton(text=emoji.emojize("EUR :euro_banknote:"), callback_data='eur')
        btn3 = types.InlineKeyboardButton(text=emoji.emojize("RUB :Russia:"), callback_data='rub')
        markup.add(btn1, btn2, btn3)
        bot.send_message(call.message.chat.id, text=emoji.emojize(':money-mouth_face:')*9, reply_markup=markup)
    if call.data == 'rub_sell':
        photo = open('img/rubli.jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo)
        fact = choice(clear_facts).replace("\n", " ")
        bot.send_message(call.message.chat.id, text=fact)
        bot.send_message(call.message.chat.id, '\n'.join(map(str, res_rub_sell)))
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text=emoji.emojize("USD :dollar_banknote:"), callback_data='usd')
        btn2 = types.InlineKeyboardButton(text=emoji.emojize("EUR :euro_banknote:"), callback_data='eur')
        btn3 = types.InlineKeyboardButton(text=emoji.emojize("RUB :Russia:"), callback_data='rub')
        markup.add(btn1, btn2, btn3)
        bot.send_message(call.message.chat.id, text=emoji.emojize(':money-mouth_face:')*9, reply_markup=markup)


bot.infinity_polling()


