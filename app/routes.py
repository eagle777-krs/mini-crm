from forms import LoginForm, RegisterForm, UserForm, ClientForm, DealForm
from flask import Blueprint, render_template, redirect, url_for, flash, get_or_404
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Client, Deal, db
from sqlalchemy import func, extract

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
    top_10_deals = Deal.query.order_by(Deal.amount).limit(10).all()
    return render_template('index.html', deals=top_10_deals)

@main.route('/user_page/<id>', methods=['GET'])
@login_required
def user_page(id):
    user = User.query.get(current_user.id)
    user_deals = Deal.query.filter(Deal.user_id == current_user.id).order_by(Deal.amount).all()
    return render_template(
        'user_page.html',
        user=user,
        user_deals = user_deals
    )

@main.route('/clients', methods=['GET'])
@login_required
def clients():
    clients = Client.query.order_by(Client.name).all()
    return render_template(
        'clients.html',
        clients = clients
    )

@main.route('/client_page/<id>', methods=['GET'])
@login_required
def client_page(id):
    client_info = Client.query.filter(Client.id == id).first()
    return render_template(
        'client_page.html',
        client_info = client_info
    )

@main.route('/client_page/add', methods=['GET', 'POST'])
@login_required
def add_client_page(id):
    form = ClientForm()

    if form.validate_on_submit():
        new_client = Client()
        form.populate_obj(new_client)
        db.session.add(new_client)
        db.session.commit()
        flash('Клиент добавлен')
        return redirect(url_for('main.clients'))
    return render_template('client_form.html', form=form, submit_text='Добавить')

@main.route('/client_page/edit/<id>', methods=['GET', 'POST'])
@login_required
def update_client_page(id):
    client = Client.get_or_404(id)
    form = ClientForm(obj=client)

    if form.validate_on_submit():
        form.populate_obj(client)
        db.session.commit()
        flash('Клиент обновлён')
        return redirect(url_for('main.client_page', id=client.id))
    return render_template('client_form.html', form=form, submit_text='Сохранить')

@main.route('/client_page/delete/<id>', methods=['POST'])
@login_required
def delete_client_page(id):
    client = Client.get_or_404(id)
    db.session.delete(client)
    db.commit()
    flash('Клиент был удалён')
    return redirect(url_for('main.clients'))

@main.route('/deals', methods=['GET'])
@login_required
def deals():
    deals = Deal.query.all()
    return render_template(
        'deals.html',
        deals=deals
    )

@main.route('/deal_page/add', methods=['GET', 'POST'])
@login_required
def add_deal_page(id):
    form = DealForm()

    if form.validate_on_submit():
        new_deal = Deal()
        form.populate_obj(new_deal)
        db.session.add(new_deal)
        db.session.commit()
        flash('Сделка добавлен')
        return redirect(url_for('main.deals'))
    return render_template('deal_form.html', form=form, submit_text='Добавить')

@main.route('/deal_page/<id>', methods=['GET'])
@login_required
def deal_page(id):
    deal = Deal.query.filter(Deal.id == id).first()
    return render_template(
        'deal.html',
        deal=deal
    )

@main.route('/deal_page/edit/<id>', methods=['GET', 'POST'])
@login_required
def update_deal_page(id):
    deal = Deal.query.get_or_404(id)
    form = DealForm(obj=deal)

    if form.validate_on_submit():
        form.populate_obj(deal)
        db.session.commit()
        flash('Сделка обновлена', 'success')
        return redirect(url_for('deal_page', id=deal.id))

    return render_template('deal_form.html', form=form, submit_text='Сохранить изменения')

@main.route('/deal_page/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_deal_page(id):
    deal = Deal.query.get_or_404(id)
    db.session.delete(deal)
    db.session.commit()
    flash('Сделка удалена', 'success')
    return redirect(url_for('deals'))

@main.route('/analytics', methods=['GET'])
@login_required
def analytics():
    # Общая выручка (все сделки по amount)
    total_revenue = db.session.query(func.sum(Deal.amount)).scalar() or 0
    # Средняя сумма сделки
    avg_deal = db.session.query(func.avg(Deal.amount)).scalar() or 0
    # Количество клиентов и сделок
    total_clients = db.session.query(func.count(Client.id)).scalar()
    total_deals = db.session.query(func.count(Deal.id)).scalar()
    # Топ-5 клиентов по объёму сделок (sales_volume из модели Client)
    top_clients = (
        db.session.query(Client.name, func.sum(Deal.amount).label('total'))
        .join(Deal, Deal.client_id == Client.id)
        .group_by(Client.id, Client.name)
        .order_by(func.sum(Deal.amount).desc())
        .limit(5)
        .all()
    )
    # График: сумма сделок по месяцам (из date_start)
    monthly_stats = (
        db.session.query(
            extract('month', Deal.date_start).label('month'),
            func.sum(Deal.amount).label('monthly_sum')
        )
        .group_by('month')
        .order_by('month')
        .all()
    )
    month_labels = [f'{int(row.month):02d}' for row in monthly_stats]
    month_values = [float(row.monthly_sum) for row in monthly_stats]

    return render_template(
        'analytics.html',
        total_revenue=total_revenue,
        avg_deal=avg_deal,
        total_clients=total_clients,
        total_deals=total_deals,
        top_clients=top_clients,
        month_labels=month_labels,
        month_values=month_values
    )