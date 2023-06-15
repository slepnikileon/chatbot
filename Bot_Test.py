import telebot
from datetime import date, datetime, time, timedelta
import pyodbc
import time
from telebot import types


#Подключение к БД
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ET-00012\EMCI_DEV;'
                      'Database=Amosov;'
                      'Trusted_Connection=yes;')

bot = telebot.TeleBot('1698654483:AAG4dMcgLxKAE46aRYQ1x9fqvb-gQiYu5jc')

cursor = conn.cursor()

#Клавиатура основная
keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row( telebot.types.InlineKeyboardButton('Сообщить об ошибке', callback_data='Error'),
              telebot.types.InlineKeyboardButton('Оставить пожелание', callback_data='2'))

#Клавиатура цй этап
keyboard_edit = telebot.types.InlineKeyboardMarkup()
keyboard_edit.row( telebot.types.InlineKeyboardButton('Документ', callback_data='Doc'),
                  telebot.types.InlineKeyboardButton('Отчет', callback_data='Report'))
keyboard_edit.row( telebot.types.InlineKeyboardButton('Интерфейс', callback_data='Int'),
                  telebot.types.InlineKeyboardButton('Ehelth', callback_data='Ehelth'))
keyboard_edit.row( telebot.types.InlineKeyboardButton('Запуск', callback_data='Start'),
                  telebot.types.InlineKeyboardButton('Другое', callback_data='Other'))

#Клавиатура Детали
keyboard_edit2 = telebot.types.InlineKeyboardMarkup()
keyboard_edit2.row( telebot.types.InlineKeyboardButton('Скрин', callback_data='Screen'),
              telebot.types.InlineKeyboardButton('Описание', callback_data='opys'))


#Старт Бота
@bot.message_handler(commands=["3817"])
def start_message(message):
    user_Name = str(message.from_user.first_name)
    bot.send_message(message.chat.id, 'Привіт, '+ user_Name +'! \nДававйте спочатку перевіримо чи зареєстровані ви. Вкажіть номер телефону у форматі +380*********.')  #, reply_markup=keyboard
    #bot.send_message(message.chat.id, 'Привіт, '+ user_Name +'! \nЧто именно нужно?)', reply_markup=keyboard)    

#Оброботчик CallBack(Клавыатуры_ID)
@bot.callback_query_handler(func=lambda call: True)
def callback_func(qwery):
  global value
  data = qwery.data
  global stat, status_d

  if data == 'Error':
    #global Error_back
    #Error_back = data
    bot.send_message(qwery.message.chat.id, 'Укажите в каком модуле ошибка или с чем связано:\n\n\n', reply_markup=keyboard_edit)
  
  if data == 'Doc':
    stat = 'Doc'
    bot.send_message(qwery.message.chat.id, 'Укажите название документа:\n\n\n')

  if data == 'Report':
    stat = 'Report'
    bot.send_message(qwery.message.chat.id, 'Укажите название отчета:\n\n\n')
  
  if data == 'Screen':
    status_d = 'Screen'
    bot.send_message(qwery.message.chat.id, 'Добавьте скрин:\n\n\n')
  
  if data == 'opys':
    status_d = 'opys'
    bot.send_message(qwery.message.chat.id, 'Укажите описание:\n\n\n')


@bot.message_handler(content_types=['text'])
def get_text_messages_1(message):
  global feedback_phone
  feedback_phone = message.text #.lower()
  if feedback_phone is not None:
    sqlqwery = cursor.execute ("SELECT pn.FullName FROM PersonNames pn INNER JOIN Phones p ON pn.PersonID = p.PersonID WHERE pn.Status = 'L' and p.PhoneNumber = '"+ feedback_phone +"'").fetchone()
    if sqlqwery is not None:
      mesg12 = bot.send_message(message.chat.id,'Так ви зареєстровані як ' + sqlqwery[0] + '\nЩо саме потрібно?)', reply_markup=keyboard) #
      bot.register_next_step_handler(mesg12,Phone)
    else:
      bot.send_message(message.chat.id,'Вы не зареэстровані або вказали невірно номер. Зверніться до адміністратора.') 

def Phone(message):
  global feedback
  feedback = message.text #.lower()

#Нужно оптимизировать  
  if stat == 'Doc' and feedback is not None:
    sqlqwery = cursor.execute ("select top 1 dbo.fnGetStrForLang(ma.ActName, dbo.fnGetSYSLang()) FROM MedActs ma WHERE dbo.fnGetStrForLang(ma.ActName, dbo.fnGetSYSLang()) LIKE '"+ feedback +"'").fetchone()
    if sqlqwery is not None and sqlqwery[0] == feedback: #stat == 'Report' and
      mesg = bot.send_message(message.chat.id,'Документ знайдено! Вкажіть опис')
      bot.register_next_step_handler(mesg,Opys)
    else:
      mesg = bot.send_message(message.chat.id,'Такий документ не знайдено! Вкажіть повну назву документу.')
  
  
  
  
  elif  stat == 'Report' and feedback is not None:
    sqlqwery = cursor.execute ("select sr.StatName from StatReports sr WHERE sr.StatName LIKE  '"+ feedback +"'").fetchone()
    if sqlqwery is not None and sqlqwery[0] == feedback:
      mesg = bot.send_message(message.chat.id,'Звіт знайдено! Вкажіть опис')
      #print (sqlqwery[0])
      bot.register_next_step_handler(mesg,Opys)
    else:
      mesg = bot.send_message(message.chat.id,'Такий звіт не знайдено! Вкажіть повну назву звіту.')
      #print (sqlqwery)

      



 
  
def Opys(message):
  global message_back, message_back_photo
  message_back = message.text
  Standart_back = 'Заявка прийнята!'
  global Error_type
  Error_type = stat
  #qwery = cursor.execute ("INSERT INTO Chat_bot (CrDate, Type, TypeError, Name, Opys, Login, Phone) VALUES (GetDate(), '" + Error_back + "', '" + Error_type + "', '" + feedback + "', N'" + message_back + "', '" + message.from_user.first_name + "', '" + message_back1 + "')")
 # if qwery is not None:
  bot.send_message(message.chat.id, 'Готово')

  if message_back is not None and stat == 'Doc':
    bot.send_message(message.chat.id,Standart_back + '\n\n' + 'Документ\n' + feedback + '\n\nОпис\n' + message_back )
    mesg1 = bot.send_message(message.chat.id,'Продублюйте свій номер телефона або вкажіть пошту?')
    bot.register_next_step_handler(mesg1,contact)
  
  elif message_back is not None  and stat == 'Report':
    bot.send_message(message.chat.id,Standart_back + '\n\n' +'Звіт\n' + feedback + '\n\nОпис\n' + message_back)
    mesg1 = bot.send_message(message.chat.id,'Продублюйте свій номер телефона або вкажіть пошту?')
    bot.register_next_step_handler(mesg1,contact)
  else:
    bot.send_message(message.chat.id,'Не хватает данных\n\n\n')


def contact(message):
  message_back1 = message.text
  if message_back1 is not None: # and len(message_back1) >= 13:
    qwery = cursor.execute ("INSERT INTO Chat_bot (CrDate, Type, TypeError, Name, Opys, Login, Phone) VALUES (GetDate(), '" + Error_back + "', '" + Error_type + "', '" + feedback + "', N'" + message_back + "', '" + message.from_user.first_name + "', '" + message_back1 + "')")
    if qwery is not None:
      bot.send_message(message.chat.id, 'Готово')
    #print(Error_back,Error_type,back,message_back,message_back1)
  #else:
   # bot.send_message(message.chat.id, 'Телефон должен біть в формате "+3801234567890"')

  conn.commit()
#cursor.close()
bot.polling(none_stop=True, interval=0)
