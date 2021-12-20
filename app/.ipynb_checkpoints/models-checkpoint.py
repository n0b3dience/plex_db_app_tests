"""
Database Models
"""


from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=0)
    nickname = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    known_ips = db.Column(db.String(2000), nullable=True)
    # user_image = db.Column(db.String(), nullable=True)
    # posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return '<User {0!r}>'.format(self.username)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.String(2000))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime)
    votes = db.Column(db.Integer, default=0)
    is_live = db.Column(db.Boolean, default=1)

    def __repr__(self):
        return '<Post: {0!r}>'.format(self.title)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2000))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_added = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    last_updated = db.Column(db.DateTime())
    votes = db.Column(db.Integer, default=0)
    post_id = db.Column(db.Integer, nullable=True)
    is_live = db.Column(db.Boolean, default=1)
    parent_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<{0!r}>'.format(self.text)


# Post/comment closure table
class PostComment(db.Model):
    __tablename__ = 'post_comment'
    pk = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    comment_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<post_id : {0!r} | comment_id : {1!r}>'.format(
            self.post_id, self.comment_id)


# Comment closure table
class ParentChild(db.Model):
    __tablename__ = 'parent_child'
    pk = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, nullable=True)
    id = db.Column(db.Integer, nullable=False)
    child_id = db.Column(db.Integer,nullable=True)
    post_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<post_id : {0!r} | parent_id : {1!r} | id : {2!r} | child_id : {3!r}>'.format(
            self.post_id, self.parent_id, self.id, self.child_id)
    
