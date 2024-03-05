from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from blog import db, app, login_manager


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(user_id)


class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False, unique=True)
    email = Column(String(60), nullable=False, unique=True)
    password = Column(String(30), nullable=False)
    posts = relationship('PostModel', backref='auther', lazy=True)

    def __repr__(self):
        return f'User({self.username}, {self.email})'


class PostModel(db.Model):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    date = Column(DateTime, default=datetime.now)
    auther_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'Post({self}, {self.title[:20]}, {self.date})'


with app.app_context():
    db.create_all()
