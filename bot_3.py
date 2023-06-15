import telebot
import pyodbc
import time
from telebot import types
#Подключение к БД
conn = pyodbc.connect('Driver={SQL Server};'
                      ''
                      'Database=bot;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

bot = telebot.TeleBot('')

value = ''
bol = ''

#(map(str, row1))
#Запрос в БД
ttt = cursor.execute ('SELECT id FROM dbo.acces')
#for row in ttt:
row1 = cursor.fetchall()
#Убрать левые символы 
#for resu in row1:
results = ' '.join(map(str, row1))
result = str(results).replace("(", "")
result = str(result).replace(")", "")
result = str(result).replace(",", "")
result = str(result).replace(" ", "")
print (ttt)

#Клавиатура основная
keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row( telebot.types.InlineKeyboardButton('Черкассы', callback_data=result[0]),
              telebot.types.InlineKeyboardButton('Бахмут', callback_data=result[1]),
              telebot.types.InlineKeyboardButton('Киев', callback_data='3'))
keyboard.row( telebot.types.InlineKeyboardButton('Бердянск', callback_data='4'),
              telebot.types.InlineKeyboardButton('Михайловка', callback_data=result[6]),
              telebot.types.InlineKeyboardButton('Мелитополь', callback_data=result[7]))
#keyboard.row( telebot.types.InlineKeyboardButton('Новости', callback_data='Новости'))
#keyboard.row( telebot.types.InlineKeyboardButton('EMCI', callback_data='EMCI'))
keyboard.row( telebot.types.InlineKeyboardButton('Инструкции', callback_data='инстр'))

keyboard_menu = telebot.types.InlineKeyboardMarkup()
keyboard_menu.row( telebot.types.InlineKeyboardButton('Назад', callback_data='back'))
keyboard_menu.row( telebot.types.InlineKeyboardButton('Начальное меню', callback_data='menu'))



#Старт Бота
@bot.message_handler(commands=["3817"])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, '+ str(message.from_user.first_name) +'! \nЯ бот для быстрого поиска доступа разных объектов. \n\nВыбирай город или давай почитаем новости', reply_markup=keyboard)
#Оброботчик CallBack(Клавыатуры)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(qwery):
  global value
  data = qwery.data

  if data in set(result):
    sqlqwery = cursor.execute ('''SELECT * FROM dbo.acces WHERE id = ?''', data)
    if data == '3':
      keyboard_1 = telebot.types.InlineKeyboardMarkup()
      keyboard_1.row( telebot.types.InlineKeyboardButton('КМКЛ 17', callback_data=result[2]),
                  telebot.types.InlineKeyboardButton('КМКЛ 18', callback_data=result[3]))
      bot.send_message(qwery.message.chat.id, 'Вот, что нашлось в городе ' + data, reply_markup=keyboard_1)
    
    if data == '4':
      keyboard_1 = telebot.types.InlineKeyboardMarkup()
      keyboard_1.row( telebot.types.InlineKeyboardButton('БТМО', callback_data=result[4]),
                  telebot.types.InlineKeyboardButton('ЦПМСД', callback_data=result[5]))
      bot.send_message(qwery.message.chat.id, 'Вот, что нашлось в городе ' + data, reply_markup=keyboard_1)

    else:
      for row in sqlqwery:
        tes = "\nIP: " + row[2] + "\nLogin: " + row[3] + "\nPassword: " + row[4]
        bot.send_message(qwery.message.chat.id, 'Вот, что нашлось в городе ' + str(tes))
        #time.sleep(1)
        bot.send_message(qwery.message.chat.id, 'Что еще?', reply_markup=keyboard_menu)

  if data == 'инстр':
    text = '[Инструкции \n тут превью и тд ](https://drive.google.com/drive/folders/1gP8hQD3G5xtEx9h0OEmQmqYG5erWZxMi)'
    bot.send_message(qwery.message.chat.id, text, parse_mode='Markdown')
    #time.sleep(1)
    bot.send_message(qwery.message.chat.id, 'Что еще?', reply_markup=keyboard)
  
  if data == 'back':
  #time.sleep(1)
    bot.send_message(qwery.message.chat.id, 'OK', reply_markup=keyboard_menu)

  if data == 'EMCI':
    keyboard_1 = telebot.types.InlineKeyboardMarkup()
    keyboard_1.row( telebot.types.InlineKeyboardButton('Обучающие видео', callback_data='Обучающие видео'),
                    telebot.types.InlineKeyboardButton('Сайт', callback_data='Сайт'))
    bot.send_message(qwery.message.chat.id, 'Что дальше?', reply_markup=keyboard_1)

  elif data == 'Обучающие видео':
    text = '[Видосики (test)](https://youtube.com/channel/UC82q7HRaxyK4yF5XPHIJ5lw)'
    bot.send_message(qwery.message.chat.id, text, parse_mode='Markdown')
    #time.sleep(1)
    bot.send_message(qwery.message.chat.id, 'Что еще?', reply_markup=keyboard)
  elif data == 'Сайт':
    text = '[Сайт TMCI ](https://emci.ua/)'
    bot.send_message(qwery.message.chat.id, text, parse_mode='Markdown')
    #time.sleep(1)
    bot.send_message(qwery.message.chat.id, 'Что еще?', reply_markup=keyboard)

bot.polling(none_stop=True, interval=0)
