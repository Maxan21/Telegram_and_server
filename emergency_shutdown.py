from subprocess import check_output
import telebot
from telebot import types
import time
import sys
import random
import logging
level = logging.DEBUG
FORMAT = '%(asctime)s %(processName)s\%(name)-8s %(levelname)s: %(message)s'
logfile = '/root/my.log'
logging.basicConfig(format = FORMAT, level=level, filename = logfile )

logger = logging.getLogger(__name__)
debug = logger.debug
print = logger.info

start_time=time.time()
bot = telebot.TeleBot("") #токен бота
bool1=True

user_id=[]

@bot.message_handler(commands=['start'])
def start(message):
    try:
        if check_output('systemctl status openvpn-server@server.service', shell=True) and  'Active: active (running)' in check_output('systemctl status openvpn-server@server.service', shell=True).decode('utf-8'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Выключить 🙈")
            btn2 = types.KeyboardButton("Приостановить 🙊")
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, 'Сервер активен', reply_markup=markup)
    except Exception as e: 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Выключить 🙈")
        btn2 = types.KeyboardButton("Восстановить 🙉")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Сервер приостановлен', reply_markup=markup)
@bot.message_handler(content_types=['text'])
def main(message):
    global bool1, start_time
    try:
        check=check_output('systemctl status openvpn-server@server.service', shell=True)
        check = check.decode('utf-8')
        if message.chat.id in user_id and  message.text=='Приостановить 🙊' and 'Active: active (running)' in check:
            k=bot.send_message(message.chat.id, 'Дождитесь сообщения об успешном выполнении🫡') 
            check_output('sudo systemctl stop  openvpn-server@server.service\nsudo systemctl stop openvpn.service\nsudo systemctl stop openvpn-iptables.service\ndocker stop watchtower\ndocker stop shadowbox', shell=True) 
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
            btn1 = types.KeyboardButton("Восстановить 🙉") 
            markup.add(btn1)
            bot.delete_message(message.chat.id,k.message_id) 
            bot.send_message(message.chat.id,'Приостановлено...', reply_markup=markup)
        elif message.chat.id in user_id and message.text=='Приостановить 🙊':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Восстановить 🙉")
            markup.add(btn1)
            bot.send_message(message.chat.id,'Кто-то уже приостановил работу🤥', reply_markup=markup)
        elif message.chat.id in user_id and message.text=='Подтвердить операцию':
            comand = 'shutdown now'  
            bot.delete_message(message.chat.id,check.message_id)
            try:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Выключить 🙈")
                btn2 = types.KeyboardButton("Приостановить 🙊")
                markup.add(btn1, btn2)
                bot.send_message(message.chat.id, check_output(comand, shell = True),reply_markup=markup )
            except: 
                bot.send_message(message.chat.id, "Invalid input") 
        elif message.chat.id in user_id and message.text=='Выключить 🙈':
            if time.time()-start_time<300:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                a=random.randint(0,1)
                A=["Подтвердить операцию", "Вернуться в главное меню"]
                btn1 = types.KeyboardButton(A[a])
                btn2 = types.KeyboardButton(A[1-a])
                markup.add(btn1, btn2)
                check=bot.send_message(message.chat.id, text="Бот перестанет функционировать при команде 'Выключить'\nВы уверены?", reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Выключить 🙈")
                btn2 = types.KeyboardButton("Приостановить 🙊")
                markup.add(btn1, btn2)
                bot.send_message(message.chat.id, check_output('shutdown now', shell = True), reply_markup=markup)
        elif message.chat.id in user_id and message.text=="Вернуться в главное меню":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Выключить 🙈")
            btn2 = types.KeyboardButton("Приостановить 🙊")
            markup.add(btn1, btn2)
            bot.delete_message(message.chat.id,check.message_id)
            bot.send_message(message.chat.id, "😰", reply_markup=markup)
        elif message.chat.id in user_id and message.text=='Восстановить 🙉':
            if 'Active: active (running)' not in check:
                k=bot.send_message(message.chat.id, 'Дождитесь сообщения об успешном выполнении🫡')
                check_output('sudo systemctl start openvpn-server@server.service\nsudo systemctl start openvpn.service\nsudo systemctl start openvpn-iptables.service\ndocker start watchtower\ndocker start shadowbox',shell = True)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Выключить 🙈")
                btn2 = types.KeyboardButton("Приостановить 🙊")
                markup.add(btn1, btn2)
                bool1=True
                bot.delete_message(message.chat.id,k.message_id)
                bot.send_message(message.chat.id,'Восстановлено🥵',reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Выключить 🙈")
                btn2 = types.KeyboardButton("Приостановить 🙊")
                markup.add(btn1, btn2)

                bot.send_message(message.chat.id, "Кто-то уже восстановил работу🤓", reply_markup=markup) 


        else:
            bot.send_message(message.from_user.id, 'Доступ закрыт')
    except Exception as e:
        if message.chat.id in user_id and message.text=='Приостановить 🙊':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Восстановить 🙉")
            markup.add(btn1)
            bot.send_message(message.chat.id,'Кто-то уже приостановил работу🤥', reply_markup=markup)
        elif message.chat.id in user_id and message.text=='Подтвердить операцию':
            comand = 'shutdown now'  
            bot.delete_message(message.chat.id,check.message_id)
            try:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Выключить 🙈")
                btn2 = types.KeyboardButton("Приостановить 🙊")
                markup.add(btn1, btn2)
                bot.send_message(message.chat.id, check_output(comand, shell = True),reply_markup=markup )
            except: 
                bot.send_message(message.chat.id, "Invalid input") 
        elif message.chat.id in user_id and message.text=='Выключить 🙈':
            if time.time()-start_time<300:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                a=random.randint(0,1)
                A=["Подтвердить операцию", "Вернуться в главное меню"]
                btn1 = types.KeyboardButton(A[a])
                btn2 = types.KeyboardButton(A[1-a])
                markup.add(btn1, btn2)
                check=bot.send_message(message.chat.id, text="Бот перестанет функционировать при команде 'Выключить'\nВы уверены?", reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Выключить 🙈")
                btn2 = types.KeyboardButton("Приостановить 🙊")
                markup.add(btn1, btn2)
                bot.send_message(message.chat.id, check_output('shutdown now', shell = True), reply_markup=markup)
        elif message.chat.id in user_id and message.text=="Вернуться в главное меню":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Выключить 🙈")
            btn2 = types.KeyboardButton("Приостановить 🙊")
            markup.add(btn1, btn2)
            bot.delete_message(message.chat.id,check.message_id)
            bot.send_message(message.chat.id, "😰", reply_markup=markup)
        elif message.chat.id in user_id and message.text=='Восстановить 🙉':
            k=bot.send_message(message.chat.id, 'Дождитесь сообщения об успешном выполнении🫡')
            check_output('sudo systemctl start openvpn-server@server.service\nsudo systemctl start openvpn.service\nsudo systemctl start openvpn-iptables.service\ndocker start watchtower\ndocker start shadowbox',shell = True)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Выключить 🙈")
            btn2 = types.KeyboardButton("Приостановить 🙊")
            markup.add(btn1, btn2)
            bool1=True
            bot.delete_message(message.chat.id,k.message_id)
            bot.send_message(message.chat.id,'Восстановлено🥵',reply_markup=markup)
        else:
            bot.send_message(message.from_user.id, 'Доступ закрыт')


if __name__ == '__main__':
    while True:
        try: #добавляем try для бесперебойной работы
            bot.polling(none_stop=True) #запуск бота
        except:
            time.sleep(10) #в случае падения


sys.stdout = LoggerWriter(logger.info)
sys.stderr = LoggerWriter(logger.warning)
