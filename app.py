from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Post
from forms import RegistrationForm, LoginForm, PostForm
import os

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))   # 从环境变量读取端口，默认5000
    app.run(host="0.0.0.0", port=port, debug=True)


app = Flask(__name__)
app.config['SECRET_KEY'] = '你的随机密钥，请更换为实际值'
app.config['WTF_CSRF_ENABLED'] = False  # 开发调试时可暂时关闭 CSRF
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 绑定 SQLAlchemy 实例
db.init_app(app)

# 登录管理
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 首页：文章列表
@app.route('/')
def home():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('index.html', articles=posts)


# 文章详情
@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('用户名已存在', 'danger')
        else:
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('注册成功，请登录', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('登录成功', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        flash('用户名或密码错误', 'danger')
    return render_template('login.html', form=form)

# 登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已登出', 'info')
    return redirect(url_for('home'))

# 新建文章
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('文章发布成功', 'success')
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('new_post.html', form=form)

# 删除文章
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.id and not current_user.is_admin:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('文章已删除', 'info')
    return redirect(url_for('home'))

# 程序入口
#if __name__ == '__main__':
   # with app.app_context():
    #    db.create_all()
   # app.run(debug=True)
   

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))   # 从环境变量读取端口，默认5000
    app.run(host="0.0.0.0", port=port, debug=True)
