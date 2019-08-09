#-- coding: utf-8 --
"""
This Example will show you how to use register_next_step handler.
"""
import requests
import telebot
from telebot import types
import MySQLdb #BIBLIOTECA MYSQL
import urllib
import json


con = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='teste') #CONEXAO AO BANCO
con.select_db('teste') ##SELECIONA O BANCO
 
cursor = con.cursor() #CONECTA NO BANCO

API_TOKEN = ''

bot = telebot.TeleBot(API_TOKEN)


user_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.time = None
       


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	
    msg = bot.reply_to(message, """\
Olá, eu sou o Bot de notícias do seu time!

""")
    cid = message.chat.id
    bot.send_message(cid, "Nosso id: " + str(cid) + " Isso serve para que eu consiga lhe enviar as notícias!, agora vamos em frente www.ricardomilbrath.com.br !\n Qual o seu nome?")
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Quantos anos você tem?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'a idade precisa ser um número. Quantos anos você tem?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Gremio', 'Internacional')
        msg = bot.reply_to(message, 'Qual o seu time do Coração?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


       

def process_sex_step(message):
    try:
        chat_id = message.chat.id
        time = message.text
        user = user_dict[chat_id]
        if (time == u'Gremio') or (time == u'Internacional'):
            user.time = time
        else:
            raise Exception()

        #sql = "INSERT INTO clientes (nome,idade,sexo) VALUES (%s,%i,%s)" # SQL  PARA INSERCAO DOS DADOS NO BANCO
        #val = (user.name,user.age,user.sex) # VARIAVEL QUE SERA INSERIDA COM TODA A MENSAGEM VINDA DO TELEGRAM
        cursor.execute("INSERT INTO clientes (chat_id, nome, idade, time_fut) VALUES (%s, %s, %s, %s)", (chat_id, user.name, user.age, user.time)) #EXECUTA A INSERCAO DE FATO
        con.commit() # FAZ O COMMIT NO BANCO CONFIRMANDO A INSERCAO
        bot.send_message(chat_id, 'Prazer ' + user.name + '\n Idade: ' + str(user.age) + '\n Time: ' + user.time + '\n Nosso id: ' + str(chat_id))
        
    except Exception as e:
        bot.reply_to(message, e)


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling()

