from flask import Flask, render_template, request, logging, Response, redirect, flash

# Flask の起動
app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"]) # hoge.com/にアクセスした時に実行される関数
def index():
    if request.method == 'POST':
        user_id = request.form['user_id'] # formのname = "user_id"を取得
        return render_template('index.html', user_id = user_id) # index.htmlを呼び出す
    else:
        return render_template('index.html')
app.run(host="localhost")
