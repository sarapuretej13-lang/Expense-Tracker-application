from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import calendar


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship: one user has many expenses
    expenses = db.relationship('Expense', backref='owner', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'amount': self.amount,
            'category': self.category,
            'date': self.date.strftime('%Y-%m-%d'),
            'notes': self.notes,
        }

    def __repr__(self):
        return f'<Expense {self.title} - ₹{self.amount}>'


# Predefined expense categories
CATEGORIES = [
    'Food & Dining',
    'Transport',
    'Shopping',
    'Bills & Utilities',
    'Entertainment',
    'Health & Medical',
    'Education',
    'Travel',
    'Rent & Housing',
    'Personal Care',
    'Savings & Investment',
    'Other',
]


class Budget(db.Model):
    __tablename__ = 'budgets'

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount     = db.Column(db.Float, nullable=False)          # monthly budget in ₹
    month      = db.Column(db.Integer, nullable=False)        # 1-12
    year       = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'month', 'year', name='uq_budget_user_month_year'),
    )

    def __repr__(self):
        return f'<Budget ₹{self.amount} for {calendar.month_abbr[self.month]} {self.year}>'
