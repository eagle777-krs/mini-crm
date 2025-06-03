from crypt import methods

from forms import LoginForm, RegisterForm, UserForm, ClientForm, DealForm
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Client, Deal, db

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.user_page', id=current_user.id))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('main.user_page', id=current_user.id))
        flash('Неверное имя пользователя или пароль', 'danger')
    return render_template('login.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Пользователь создан! Войдите в систему.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/')
def index():
    return "Hello from Flask!"

@main.route('/user_page/<id>', methods=['GET'])
def user_page(id):
    pass

@main.route('/clients', methods=['GET'])
def clients():
    pass

@main.route('/client_page/<id>', methods=['GET'])
def client_page(id):
    pass

@main.route('/client_page/edit/<id>', methods=['GET', 'POST'])
def update_client_page(id):
    pass

@main.route('/client_page/delete/<id>', methods=['GET', 'POST'])
def delete_client_page(id):
    pass

@main.route('/deals', methods=['GET'])
def deals():
    pass

@main.route('/deal_page/<id>', methods=['GET'])
def deal_page(id):
    pass

@main.route('/deal_page/edit/<id>', methods=['GET', 'POST'])
def update_deal_page(id):
    pass

@main.route('/deal_page/delete/<id>', methods=['GET', 'POST'])
def delete_deal_page(id):
    pass

@main.route('/analytics', methods=['GET'])
def analytics():
    pass