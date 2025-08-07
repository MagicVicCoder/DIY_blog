# models.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# 在这里创建 db 实例，但不绑定到任何 app
db = SQLAlchemy()

class User(db.Model, UserMixin):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, raw):
        self.password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)

    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    title     = db.Column(db.String(200), nullable=False)
    content   = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author    = db.relationship('User', backref='posts')
    created   = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Post {self.title}>'
