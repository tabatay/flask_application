from flask import Flask, render_template, request, logging, Response, redirect, flash

# Flask の起動
app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"]) # hoge.com/にアクセスした時に実行される関数
def index():
    if request.method == 'POST':
        show_text = request.form['show_text'] # formのname = "show_text"を取得
        return render_template('index.html', show_text = show_text) # index.htmlを呼び出す
    else:
        return render_template('index.html')
app.run(host="localhost")
