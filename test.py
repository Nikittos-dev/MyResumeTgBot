import telebot;
bot = telebot.TeleBot('-----------------------------------------------') # token bots
from telebot import types
import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False) #db/
cursor = conn.cursor()


name = ''
surname = ''
age = 0
country =''


@bot.message_handler(commands=['start'])
def start(message):
    namber = message.from_user.id
    if message.text =='/start':
        for reg_value in cursor.execute("SELECT id_user from test"):
            if namber in reg_value:
                 markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 button_menu = types.KeyboardButton('Меню')
                 markup.add(button_menu) #add button
                 bot.send_message(message.from_user.id,'Привет, {0.first_name}!'.format(message.from_user), reply_markup=markup)
            else:
                 markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
                 hellopbtn = types.KeyboardButton("👋 Поздороваться и начать знакомство")
                 markup.add(hellopbtn)
                 bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот ".format(message.from_user), reply_markup=markup)


def db_table_val(id_user: int ,user_name: str, user_surname: str, user_country: str, user_age: int, user_id_name: str ):#что будем запомнитать 
	cursor.execute('INSERT INTO test (id_user, user_name, user_surname, user_country, user_age, user_id_name) VALUES (?, ?, ?, ?, ?, ?)', (id_user, user_name, user_surname, user_country, user_age, user_id_name))
	conn.commit()   

@bot.message_handler(content_types=['text'])
def func(message):
    us_id = message.from_user.id
    
    
    if message.text == '👋 Поздороваться и начать знакомство' :
         bot.send_message(message.from_user.id, "Как тебя зовут?")
         
         bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    elif message.text == 'Да - это я':

         #database insert
         db_table_val(id_user=us_id, user_name=name, user_surname=surname, user_country=country, user_age=age, user_id_name= message.chat.first_name) #database insert
         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
         button_menu = types.KeyboardButton('Меню')
         markup.add(button_menu) #add button
         bot.send_message(message.from_user.id,'Я запомнил, а теперь перейдем в меню', reply_markup=markup)
    elif message.text == 'Меню':

         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
         button_senior = types.KeyboardButton('Автор 🧑‍💻')
         button_morefunc= types.KeyboardButton('Больше 🎮')
         button_resume = types.KeyboardButton('Мое резюме 🗿')
         button_other= types.KeyboardButton('Мой Git 🤓')
         markup.add(button_senior, button_morefunc, button_other, button_resume) #add button
         bot.send_message(message.from_user.id,'<<<< ❌ Меню ❌ >>>>', reply_markup=markup)


    elif message.text == 'Нет, это не я':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    elif message.text == 'Автор 🧑‍💻':
        bot.send_message(message.from_user.id, 'Контакт с автором по ' + '[ссылке](https://t.me/MikitaMi)', parse_mode='Markdown')
    elif message.text == 'Больше 🎮':
        bot.send_message(message.from_user.id, "Здесь будут ссылки на других ботов\n А пока можно глянуть игры в GP " + '[Тык](https://play.google.com/store/apps/developer?id=BrainStormStudio)', parse_mode='Markdown')
    elif message.text == 'Мое резюме 🗿':
        bot.send_message(message.from_user.id, 'Ссылка на мое резюме по ' + '[ссылке](https://hh.ru/resume/c21588f6ff06b38fbc0039ed1f4d6b32505978)', parse_mode='Markdown')
    elif message.text == 'Мой Git 🤓':
        bot.send_message(message.from_user.id, 'Ссылка на мой гит по ' + '[ссылке](https://github.com/Nikittos-dev?tab=repositories)', parse_mode='Markdown')




def get_name(message): #получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у вас фамилия?')
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько вам лет?')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    while age == 0: #проверяем что возраст изменился
        try:
             age = int(message.text) #проверяем, что возраст введен корректно            
        except Exception:
             bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
             bot.register_next_step_handler(message, get_age)
             break
        bot.send_message(message.from_user.id, 'Откуда вы?')
        bot.register_next_step_handler(message, get_country)
    
              
def get_country(message):
    global country        
    country = message.text   

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_yes = types.KeyboardButton('Да - это я')
    button_no= types.KeyboardButton('Нет, это не я')
    markup.add(button_yes, button_no) #add button
    question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+ ' и вы из '+ country+ '?'

    bot.send_message(message.from_user.id, text=question, reply_markup=markup)
    



bot.polling(none_stop=True, interval=0) # запрос на сервер c интервалом.

'''
    elif message.text == '/help': # проверка на регистрацию
        

        
            bot.send_message(message.from_user.id, 'Вот что я умею: \nМожем познакомиться, для этого напишите /reg')
       
            bot.send_message(message.from_user.id, 'Вот что можно сделать: \nПерейдем в меню /Меню')

    
    elif message.text == '/reg': # доделать проверку на регистрацию!!!!!!!!!!!!!!!
         bot.send_message(message.from_user.id, "Привет! Давай знакомиться :)\nКак тебя зовут?")
         bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name

    else:
         bot.send_message(message.from_user.id, 'Для вывода всех команд /help'); # cheak to true     
'''
