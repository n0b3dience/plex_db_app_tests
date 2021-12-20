"""
App Routes
"""

from flask import (
    render_template,
    url_for, 
    flash, 
    redirect,
    request)
from flask_login import login_user
from app import app, db, bcrypt
from app.models import User, Post, Comment, PostComment, ParentChild
from app.forms import (
    UserSignupForm, PostForm, CommentForm, ReplyForm, Reply2Form, LoginForm)
from tautulli_api import Tautulli

t = Tautulli()

@app.template_global('get_path')
def get_path(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    path = []
    if comment.parent_id:
        path.append(comment.parent_id)
        get_path(comment.parent_id)
    else:
        pass

    return path.reverse()


@app.route('/')
def home():
    req = t.get_recently_added(count=12, media_type='show')
    recently_added_shows = req["response"]["data"]["recently_added"]

    return render_template('home.html', 
        title='Home', 
        recently_added_shows=recently_added_shows)


@app.route('/user/create', methods=('GET', 'POST'))
def signup():
    form = UserSignupForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, 
            password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('You successfully registered {}'.format(user.username))
        return redirect(url_for('login'))

    return render_template('signup.html', 
        form=form,
        title="Create a New User Account")


@app.route('/user/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 
                'error')
    
    return render_template('login.html', title='Login', form=form)


@app.route('/users')
def users():
    req = t.get_users()
    data_set = req["response"]["data"]

    return render_template('users.html', 
        data_set=data_set, 
        title='Users')


# @app.route('user/<name>')
# def user(name):
#     return render_template('user/<name>', data_set=data_set, title='<name>')


@app.route('/posts')
def posts():
    posts = Post.query.filter_by(is_live=1).all()
    return render_template('posts.html', posts=posts, title="Posts")


@app.route('/post/create', methods=('GET', 'POST'))
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, text=form.content.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))

    return render_template('create.html',
        form=form, title="Create a New Post")


@app.route('/post/<int:id>/', methods=['GET'])
def post(id):
    post = Post.query.filter_by(id=id).first()
    post_comment_tbl = PostComment.query.filter_by(post_id=id).all()
    parent_child_tbl = ParentChild.query.filter_by(post_id=id).all()
    comments = Comment.query.filter_by(post_id=id).all()
    comment_form = CommentForm()
    reply_form = ReplyForm()
    reply_form_2 = Reply2Form()
    
    return render_template('post.html', 
        post_id=id,
        post=post, 
        comment_form=comment_form, 
        reply_form=reply_form,
        reply_form_2=reply_form_2,
        comments=comments,
        post_comment_tbl=post_comment_tbl,
        parent_child_tbl=parent_child_tbl)


@app.route('/<int:post_id>/comment', methods=['POST'])
def postcomment(post_id):
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        # COLLECT & SUBMIT COMMENT FORM DATA
        comment = Comment(text=comment_form.content.data, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        # COLLECT & COMMIT POST/COMMENT CLOSURE TABLE DATA
        post_comment_tbl = PostComment(post_id=post_id, 
        comment_id=comment.id)
        db.session.add(post_comment_tbl)
        db.session.commit()
        # RELOAD PAGE
        return redirect(url_for('post', id=post_id))


@app.route('/<int:post_id>/reply/parent/<int:parent_id>', methods=['POST'])
def replyparent(parent_id, post_id):
    reply_form = ReplyForm()
    if reply_form.validate_on_submit():
        # COLLECT & COMMIT REPLY FORM DATA
        reply = Comment(text=reply_form.content.data, 
            parent_id=parent_id, post_id=post_id)
        db.session.add(reply)
        db.session.commit()
        # COLLECT & COMMIT PARENT/CHILD CLOSURE TABLE DATA
        comment_reply_tbl = ParentChild(
            post_id=post_id, id=reply.id, parent_id=reply.parent_id)
        db.session.add(comment_reply_tbl)
        db.session.commit()
        # RELOAD PAGE
        return redirect(url_for('post', id=post_id))


@app.route('/<int:post_id>/reply/child/<int:parent_id>', methods=['POST'])
def replychild(parent_id, post_id):
    reply_form_2 = Reply2Form()
    if reply_form_2.validate_on_submit():
        # COLLECT & COMMIT REPLY FORM DATA
        reply = Comment(text=reply_form_2.content.data, 
            parent_id=parent_id, post_id=post_id)
        db.session.add(reply)
        db.session.commit()
        # COLLECT & COMMIT PARENT/CHILD CLOSURE TABLE DATA
        comment_reply_tbl = ParentChild(
            post_id=post_id, id=reply.id, parent_id=reply.parent_id)
        db.session.add(comment_reply_tbl)
        db.session.commit()
        # RELOAD PAGE
        return redirect(url_for('post', id=post_id))


@app.route('/post/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    form = PostForm()
    post_to_edit = Post.query.get_or_404(id)

    if request.method == 'POST':
        post_to_edit.title = request.form['title']
        post_to_edit.text = request.form['text']

        if not post_to_edit.title:
            flash('Title is required!')
        elif not post_to_edit.text:
            flash('Content is required!')
        else:
            pass
        try:
            db.session.commit()
            flash('Post updated')
            return redirect(url_for('posts'))
        except:
            flash('Looks like there was a problem. Try again.')
    
    else:
        return render_template('edit.html', form=form)


# @app.route('/post/<int:id>/delete/', methods=('POST',))
# def delete(id):
#     post = get_post(id)
#     conn = get_db_connection()
#     conn.execute('UPDATE posts SET live = 0 WHERE id = ?', (id,))
#     conn.commit()
#     conn.close()
#     flash('"{}" was successfully deleted!'.format(post['title']))
#     return redirect(url_for('posts'))


# ============
# Error Routes
# ============

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("404.html"), 500