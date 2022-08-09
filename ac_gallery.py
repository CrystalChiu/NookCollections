from flask import Flask, render_template, request_started, url_for
import requests
from requests import get

app = Flask(__name__)

#make a new page for index
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/fish/<fish_id>')
def fish(fish_id):
    response = requests.get(f"https://acnhapi.com/v1/fish/{fish_id}")
    fish_name = response.json()['file-name']

    return render_template('index.html', fish_name = fish_name) 
    #left = name of new variable in jinja template; right = value we assign to new var
    #common convention -> name them the same thing

if __name__ == '__main__':
    app.run()




