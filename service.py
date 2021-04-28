from flask import Flask, request, render_template
from similarity import find_most_similar
from main import Bot

app = Flask(__name__)
bot = Bot()

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/question', methods=['GET', 'POST'])
def return_answer(data): 
    
    answer = bot.allow_question(text=data)
    return {"answer": answer} 

if __name__ == '__main__':
    app.run(debug=True)
    # return_answer()