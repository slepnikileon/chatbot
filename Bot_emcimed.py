import telebot
from datetime import date, datetime, time, timedelta
import pyodbc
import time
#from telebot import types
#from telebot.apihelper import send_data
#import calendar
#Подключение к БД
conn = pyodbc.connect('Driver={SQL Server};'
                      ''
                      ''
                      'Trusted_Connection=yes;')

bot = telebot.TeleBot('')

cursor = conn.cursor()

#Клавиатура основная
keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row( telebot.types.InlineKeyboardButton('Записи на сьогодні', callback_data='1'),
              telebot.types.InlineKeyboardButton('Записи на завтра', callback_data='2'))
keyboard.row( telebot.types.InlineKeyboardButton('Записати пацієнта', callback_data='3'))

#Клавиатура Доп
keyboard_edit = telebot.types.InlineKeyboardMarkup()
keyboard_edit.row( telebot.types.InlineKeyboardButton('Виконано', callback_data='4'),
                  telebot.types.InlineKeyboardButton('Перенести', callback_data='5'))
keyboard_edit.row( telebot.types.InlineKeyboardButton('Редагувати', callback_data='6'),
                  telebot.types.InlineKeyboardButton('Видалити', callback_data='7'))

#Дата Сегодня с 00:00:00 по 23:59:59
currentdate = datetime.today()
SDATE = currentdate.combine(currentdate.date(), currentdate.min.time())
FDATE = currentdate.combine(currentdate.date(), currentdate.max.time())

#Дата Завтра с 00:00:00 по 23:59:59
tomorrow = currentdate + timedelta(1)
TSDATE = tomorrow.combine(tomorrow.date(), tomorrow.min.time())
TFDATE = tomorrow.combine(tomorrow.date(), tomorrow.max.time())

#print (SDATE)

#Старт Бота
@bot.message_handler(commands=["3817"])
def start_message(message):
    user_Name = str(message.from_user.first_name)
    bot.send_message(message.chat.id, 'Привіт, '+ user_Name +'! \nДавай подивимось хто записаний на сьгодні або на завтра)', reply_markup=keyboard)


#Оброботчик CallBack(Клавыатуры_ID)
@bot.callback_query_handler(func=lambda call: True)
def callback_func(qwery):
  global value
  data = qwery.data

#Условие на нажатие кнопки (1)
  if data == '1':
    sqlqwery = cursor.execute ('''SELECT pn.FullName, ra.Start, et.ETName, ra.Duration FROM RegAppointments ra INNER JOIN PersonNames pn ON ra.PatientID=pn.PersonID INNER JOIN EventTypes et ON ra.ETID = et.ETID where ra.Start BETWEEN ? AND ? AND ra.Status <> '-1' ''', SDATE, FDATE )
    res = cursor.fetchall()
    bot.send_message(qwery.message.chat.id, 'Секунду...')
    time.sleep(1)
    bot.send_message(qwery.message.chat.id, 'На сьогодні записані такі пацієнти:\n\n\n')
    for row in res:
      Name = row[0]
      Start = row[1]
      ETName = row[2]
      Duration = row[3]
      bot.send_message(qwery.message.chat.id, 'ПІБ:   ' + ' *' + str(Name) + '*' + 
                      '\nДата:   ' + ' *' + str(Start) + '*' +
                      ',\nПодія:   ' + ' *' + str(ETName) + '*' +
                      ',\nТривалість:   ' + ' *' + str(Duration) + '*' +
                      ' хв\n', reply_markup=keyboard_edit, parse_mode= 'Markdown')
    time.sleep(3)
    bot.send_message(qwery.message.chat.id, 'Спробуемо ще?', reply_markup=keyboard)

#Условие на нажатие кнопки (2) 
  if data == '2':
    sqlqwery = cursor.execute ('''SELECT pn.FullName, ra.Start, et.ETName, ra.Duration FROM RegAppointments ra INNER JOIN PersonNames pn ON ra.PatientID=pn.PersonID INNER JOIN EventTypes et ON ra.ETID = et.ETID where ra.Start BETWEEN ? AND ? AND ra.Status <> '-1' ''', TSDATE, TFDATE )
    res = cursor.fetchall()
    bot.send_message(qwery.message.chat.id, 'Секунду...')
    time.sleep(1)
    if len(res) == 0:
      bot.send_message(qwery.message.chat.id, 'Нічого не знайдено!')
      time.sleep(2)
      bot.send_message(qwery.message.chat.id, 'Спробуемо ще?', reply_markup=keyboard)  
    else:
      for row in res:
        Name = row[0]
        Start = row[1]
        ETName = row[2]
        Duration = row[3]
        bot.send_message(qwery.message.chat.id, 'ПІБ:   ' + ' *' + str(Name) + '*' + 
                      '\nДата:   ' + ' *' + str(Start) + '*' +
                      ',\nПодія:   ' + ' *' + str(ETName) + '*' +
                      ',\nТривалість:   ' + ' *' + str(Duration) + '*' +
                      ' хв\n', reply_markup=keyboard_edit, parse_mode= 'Markdown')
      time.sleep(3)
      bot.send_message(qwery.message.chat.id, 'Спробуемо ще?', reply_markup=keyboard)
  
  if data > '2':
    bot.send_message(qwery.message.chat.id, 'Функціонал поки не працюе! Оберіть щось інше', reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
