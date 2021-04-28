from pyrogram import Client
from pyrogram import filters
from main import Bot

bot = Bot()
app = Client('bot',bot_token='1741277321:AAFT8uD12rZMlnTgB-boeZ6QuASM73y_9Rg')

@app.on_message()
def find_red(client, message):
    # print(message['text'])
    try:
        app.reply_text(bot.allow_question(text=message.text)['answer'])
    except:
        pass
    
@app.on_message(filters.command('person'))
def forward_to_moderator(user):
    app.send_message('@edgaravante', "El usuario "+user+ "solicitó hablar con un humano")

    
@app.on_message(filters.command('help'))
def help(text, user):
    app.reply_text("""/help - muestra esta ayuda\n
                      /person - solicita hablar con una persona real\n
                      Para usar el bot solo escriba las preguntas
                   """)
    
def send_to_user(user, text):
    app.send_message('@edgaravante', "El usuario "+user+ "envió esta pregunta que no se pudo responder:")
    app.send_message('@edgaravante', text)

if __name__ == '__main__':
    app.run()