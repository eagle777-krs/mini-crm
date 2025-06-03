import enum
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Numeric
from sqlalchemy.orm import backref
from sqlalchemy import Enum

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    sales_volume = db.Column(Numeric(precision=10, scale=2))

    clients = db.relationship('Client', backref='salesman', lazy=True)
    deals = db.relationship('Deal', backref='salesman', lazy=True)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', sales_volume={self.sales_volume})>"


class Client(db.Model):

    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone_number = db.Column(db.String(12), unique=True)
    sales_volume = db.Column(db.Numeric(precision=10, scale=2))

    deals = db.relationship('Deal', backref='client', lazy=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}', email='{self.email}', phone_number='{self.phone_number}', sales_volume={self.sales_volume})>"


class DealType(enum.Enum):
    new = 'new'
    in_progress = 'in progress'
    waiting = 'waiting'
    canceled = 'canceled'
    closed = 'closed'

class Deal(db.Model):

    __tablename__ = 'deals'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(DealType), nullable=False)
    description = db.Column(db.String(255))
    date_start = db.Column(db.DateTime, default=datetime.utcnow)
    date_close = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return (
            f"<Deal(id={self.id}, user_id={self.user_id}, client_id={self.client_id}, "
            f"amount={self.amount}, status='{self.status.value}', "
            f"date_start={self.date_start}, date_close={self.date_close})>"
        )






