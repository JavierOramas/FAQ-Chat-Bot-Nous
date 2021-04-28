from pyrogram import Client
from pyrogram import filters
from main import Bot


app = Client('bot',
             bot_token='1741277321:AAFT8uD12rZMlnTgB-boeZ6QuASM73y_9Rg',
             api_id=1544166,
             api_hash="521282daaa5c3ac51c0a737400773fcd"
             )
bot = Bot()

@app.on_message()
def find_red(client, message):
    
    print(message)
    if message.text == '/person' or message.text == '/help':
        return
    # print(message['text'])
    
    if bot.allow_question(user=message.from_user,text=message.text) != False:
        message.reply_text(bot.allow_question(user=message.from_user,text=message.text)['answer'])
    else:
        send_to_user(message.from_user.username, message.text)
    
@app.on_message(filters.command('/person'))
def forward_to_moderator(user):
    app.send_message('@edgaravante', "El usuario "+user+ "solicitó hablar con un humano")

    
@app.on_message(filters.command('/help'))
def help(text, user, client, message):
    print('here')
    message.reply_text("""/help - muestra esta ayuda\n
                      /person - solicita hablar con una persona real\n
                      Para usar el bot solo escriba las preguntas
                   """)
    
def send_to_user(user, text):
    app.send_message('@edgaravante', "El usuario "+user+ "envió esta pregunta que no se pudo responder:")
    app.send_message('@edgaravante', text)

if __name__ == '__main__':
    app.run()