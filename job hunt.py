from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import pytz
from datetime import datetime
import os

app = Flask(__name__)

# --- 設定の修正：エラー回避とローカル優先 ---
if os.environ.get('DATABASE_URL'):
    # 本番環境（DATABASE_URLが存在する場合）
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql+psycopg://')
else:
    # ローカル環境（自分のパソコン）
    app.config["SECRET_KEY"] = os.urandom(24)
    DB_INFO = {
        'user': 'kmasa0023',    # 前のスクショのユーザー名に修正したよ！
        'password': 'K0023masa',
        'host': 'localhost',
        'name': 'job-hunt-db'   # 新しく作ったDB名
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg://{user}:{password}@{host}/{name}'.format(**DB_INFO)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# ----------------------------------------

db = SQLAlchemy(app) # まとめて初期化
migrate = Migrate(app, db)
login_manager = LoginManager(app)
tokyo_timezone = pytz.timezone('Asia/Tokyo')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    status = db.Column(db.String(50), default='エントリー中')
    event_date = db.Column(db.DateTime, nullable=True) 
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(tokyo_timezone))
    img_name = db.Column(db.String(100), nullable=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)