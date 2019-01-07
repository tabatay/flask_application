from flask import Flask, render_template, request, logging, Response, redirect, flash, session
import mysql.connector
from werkzeug import secure_filename
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime

# Flask の起動
app = Flask(__name__)

def conn_f(): # DBへの接続設定
    _conn = mysql.connector.connect(host='localhost',port=3306,user='root',db='flask_application',charset='utf8')
    return _conn

def _is_account_valid(input_username, input_password):
  
  try:
    # DBの情報を取得
    conn = conn_f()
    cursor = conn.cursor(buffered=True)
    mysql_cmd = 'select password from users where username="{0}";'.format(input_username)
    cursor.execute(mysql_cmd)
    pwd = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if check_password_hash(pwd[0], input_password):
      print("照合完了")
      return True
    else:
      return False
  except Exception as e:
    print('=== エラー内容 ===')
    print('type:' + str(type(e)))
    print('args:' + str(e.args))
    return False

# 登録後のページの表示
@app.route('/', methods=['GET','POST']) # /にアクセスすると/loginにリダイレクト
def mainpage():
  if 'user_id' in session:
    user_id = session.get('user_id')
    print('ユーザid：'+str(user_id))
    if user_id != 0:
      conn = conn_f()
      cursor = conn.cursor(buffered=True)
      mysql_cmd = 'select username, date_time from users where user_id="{0}";'.format(user_id)
      cursor.execute(mysql_cmd)
    
      username_and_datetime = cursor.fetchone()
        
      cursor.close()
      conn.close()
    
      print(username_and_datetime[0])
      print(username_and_datetime[1])

      return render_template('mainpage.html', username=username_and_datetime[0], datetime=username_and_datetime[1])
  return redirect('/login')

  #セッションがない場合はログインページにリダイレクト 
  return redirect('/login')                           

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    if _is_account_valid(request.form['username'], request.form['password']):
      
      # セッション保持のためのuser_id取得
      conn = conn_f()
      cursor = conn.cursor(buffered=True)
      mysql_cmd = 'select user_id from users where username="{0}";'.format(request.form['username'])
      cursor.execute(mysql_cmd)
      user_id = cursor.fetchone()
      session['user_id'] = user_id[0]
      
      cursor.close()
      conn.close()
      
      print('セッションidは：'+str(session.get('user_id')))
      # セッション保持
      # session['user_id'] = cursor.lastrowid
      # print('セッションidは：'+str(session.get('user_id')))
      return redirect('/')

    else:
      e_mass = "入力内容が間違っています"
      return render_template('login.html', message=e_mass)

  return render_template('login.html')

@app.route('/sign_up', methods=['GET','POST']) # /sign_upにアクセスするとsign_up.htmlを表示
# 入力結果をPOST
def sign_up():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    hash_password = generate_password_hash(password)
    date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # DBにデータを入れる
    conn = conn_f()
    cursor = conn.cursor()
    mysql_cmd = 'insert into users(username, password, date_time) values ("{0}", "{1}", "{2}");'.format(username, hash_password, date)
    cursor.execute(mysql_cmd)
    conn.commit()
    
    cursor.close()
    conn.close()
    
    session['user_id'] = cursor.lastrowid
   
    return redirect('/')

  return render_template('sign_up.html')
    
# ログアウト機能
# ユーザ情報をpopしてloginページに飛ぶ
@app.route('/logout',methods=['GET']) 
def logout():
    session.pop('user_id',None)
    return redirect('/login')

# sessionの暗号化を実施
app.secret_key='Zr9A 0/8j3yX!jmN]LWX/,?RTR~XHH'

if __name__=="__main__":
    app.run(port=8000,debug=True)

