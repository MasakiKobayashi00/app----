from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
#render_templateはきれいにするツール
from flask_migrate import Migrate
from flask_login import UserMixin,LoginManager,login_user,login_required,logout_user
from werkzeug.security import generate_password_hash,check_password_hash
import pytz#タイムゾーン取得できる
from datetime import datetime
import os

app = Flask(__name__)



login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy()

if app.debug:#ローカル環境
    "いったんランダム"
    app.config["SECRET_KEY"] = os.urandom(24)
    DB_INFO = {
    'user':'postgres',
    'password':'K0023masa',
    'host':'localhost',
    'name':'postgres'
}
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg://{user}:{password}@{host}/{name}'.format(**DB_INFO)   
#データベースの情報　＝'postgresql+psycopg://ユーザー名:パスワード@アドレス/データベースの名前'
else:#本番環境
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://','postgresql+psycopg://')

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)

migrate = Migrate(app,db)

#現在のユーザーを識別するメゾット
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):#データベースの表を作るイメージ
    id = db.Column(db.Integer,primary_key = True)#db.Column(型),db.Integerはint型,primary_key = Trueは必ず追加するという意味
    title = db.Column(db.String(100),nullable=False)#db.String(100)は文字列,()内は最大文字数,nullable=Falseは空ではないという意味
    body = db.Column(db.String(1000),nullable=False)
    tokyo_timezone = pytz.timezone('Asia/Tokyo')
    created_at = db.Column(db.DateTime,nullable=False,default = datetime.now(tokyo_timezone))#DateTimeは時間取得,default指定で投稿した時間に設定
    img_name = db.Column(db.String(100),nullable=True)#画像はパスしていやから文字列,nullable=Trueはなくてもいいという意味

class User(UserMixin,db.Model):#ログイン機能のデータベース
    id = db.Column(db.Integer,primary_key = True)#id
    username = db.Column(db.String(200),nullable=False,unique=True)#ユーザーネーム　unique=trueはかぶりを許さない
    password = db.Column(db.String(200),nullable=False)#パスワード

@app.route("/admin")#URL/のあとに整数
@login_required
def admin():#関数
    posts = Post.query.all()#保存したデータをデータベースから引っ張ってくる
    return render_template("admin.html",posts = posts)

@app.route("/create",methods = ['GET','POST'])#新規作成create
@login_required
def create():
    #1:リクエストのメゾットの判別
    if request.method == 'POST':#メゾットのポストはhtml側から送られてきたとき
    #2:リクエストできた情報の取得
        title = request.form.get('title')
        body = request.form.get('body')
        #画像の追加
        #1画像情報の取得
        file = request.files['img']
        #2画像ファイル名の取得
        filename = file.filename
        #3データベースにファイル名を保存
        post = Post(title = title,body = body,img_name = filename)
        #4画像を保存/static/img
        save_path = os.path.join(app.static_folder,'img',filename)
        file.save(save_path)

    #情報の保存
        db.session.add(post)
        db.session.commit()
    
        return redirect('/admin')#admin（管理画面）にredirect（ほかのページに飛ばす）
    elif request.method == 'GET':#メゾットのゲットはページのアクセスしたとき
        return render_template('create.html',method = 'GET')
    
@app.route("/<int:post_id>/update",methods = ['GET','POST'])#元あるものの更新update
@login_required
def update(post_id):
    post = Post.query.get(post_id)#保存したもののid
    #1:リクエストのメゾットの判別
    if request.method == 'POST':#メゾットのポストはhtml側から送られてきたとき
    #2:リクエストできた情報の取得
        post.title = request.form.get('title')#指定したidのtitle
        post.body = request.form.get('body')
        db.session.commit()#commit（更新）するだけ　　addはいらない追加はしてないから
    
        return redirect('/admin')#admin（管理画面）にredirect（ほかのページに飛ばす）
    elif request.method == 'GET':#メゾットのゲットはページのアクセスしたとき
        return render_template('update.html',method = 'GET',post = post)
    
@app.route("/<int:post_id>/delete",methods = ['GET','POST'])#元あるものの削除 delete
@login_required
def delete(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/admin')


@app.route("/signup",methods = ['GET','POST'])#ログイン
@login_required
def signup():
    #1:リクエストのメゾットの判別
    if request.method == 'POST':#メゾットのポストはhtml側から送られてきたとき
    #2:リクエストできた情報の取得
        username = request.form.get('username')
        password = request.form.get('password')
        hash_pass = generate_password_hash(password)#ユーザーが入力したパスワードをハッシュ化（暗号化)
        user = User(username = username,password = hash_pass)
 
    #情報の保存
        db.session.add(user)
        db.session.commit()
        return redirect('/login')#login画面にredirect（ほかのページに飛ばす）
    elif request.method == 'GET':#メゾットのゲットはページのアクセスしたとき
        return render_template('signup.html',method = 'GET')
    
@app.route("/login",methods = ['GET','POST'])#ログイン
def login():
    if request.method == 'POST':#メゾットのポストはhtml側から送られてきたとき
        #1ユーザー名とパスワードの受け取り
        username = request.form.get('username')
        password = request.form.get('password')
        #ユーザー名をもとにデータベースから情報を取得
        user = User.query.filter_by(username=username).first()#filter_by()検索
        #入力パスワードとデータベースのパスワードが一致してるか確認
        #一致してたらログイン→管理画面にリダイレクト、不一致→警告
        if check_password_hash(user.password,password=password):
            login_user(user)
            return redirect('/admin') 
        else:
            return redirect('/login',msg = "ユーザー名/パスワードが違います")
    elif request.method == 'GET':#メゾットのゲットはページのアクセスしたとき
        return render_template('login.html',msg = "")
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')