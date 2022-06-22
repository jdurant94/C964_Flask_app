from flask import Flask, render_template, request
import KNN

app = Flask(__name__)


KNN.knn

#homepage
@app.route('/')
def index():
    return render_template('index.html')

# sends user data to KNN to return game recs
@app.route('/submit', methods=['POST'])
def game_form_post():
    text = request.form['game']
    if text not in KNN.all_game_titles:
        return render_template('index.html', message='Please try another game')
    games_list = KNN.get_recs(text)
    return render_template('submit.html', games_list=games_list)


if __name__ == '__main__':
    app.run()
