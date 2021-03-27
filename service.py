from flask import Flask, request
from similarity import find_most_similar
from main import Bot

app = Flask(__name__)
bot = Bot()

@app.route('/')
def root():
    return '<h1> Ask a question</h1>'

@app.route('/question/<string:data>', methods=['GET', 'POST'])
def return_answer(data='person'):
    # if request.method == 'GET':
        # return '{}'
    
    # else:
    
        
    answer = bot.allow_question(text=data)
    return {"answer": answer} 

if __name__ == '__main__':
    app.run(debug=True)
    # return_answer()