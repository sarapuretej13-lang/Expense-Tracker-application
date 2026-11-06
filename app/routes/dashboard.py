from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import extract, func
from datetime import datetime, date
from collections import defaultdict
from app.models import Expense, Budget, CATEGORIES

dashboard_bp = Blueprint('dashboard', __name__)


def get_analytics(expenses):
    """Compute analytics from a list of expense objects."""
    total = sum(e.amount for e in expenses)

    # Category breakdown
    category_totals = defaultdict(float)
    for e in expenses:
        category_totals[e.category] += e.amount

    # Monthly totals
    monthly_totals = defaultdict(float)
    for e in expenses:
        key = e.date.strftime('%b %Y')
        monthly_totals[key] += e.amount

    # Sort months chronologically
    sorted_months = sorted(
        monthly_totals.items(),
        key=lambda x: datetime.strptime(x[0], '%b %Y')
    )

    # Top 5 categories for bar chart
    sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        'total': round(total, 2),
        'category_totals': dict(sorted(category_totals.items(), key=lambda x: x[1], reverse=True)),
        'monthly_labels': [m[0] for m in sorted_months],
        'monthly_values': [round(m[1], 2) for m in sorted_months],
        'bar_labels':  [c[0] for c in sorted_cats],
        'bar_values':  [round(c[1], 2) for c in sorted_cats],
    }


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    # --- Filters from query params ---
    selected_category = request.args.get('category', '')
    selected_month = request.args.get('month', '')
    sort_by = request.args.get('sort', 'date_desc')
    search_query = request.args.get('q', '').strip()

    # Base query for current user
    query = Expense.query.filter_by(user_id=current_user.id)

    # Apply filters
    if selected_category and selected_category in CATEGORIES:
        query = query.filter(Expense.category == selected_category)

    if selected_month:
        try:
            month_date = datetime.strptime(selected_month, '%Y-%m')
            query = query.filter(
                extract('year', Expense.date) == month_date.year,
                extract('month', Expense.date) == month_date.month,
            )
        except ValueError:
            pass

    if search_query:
        query = query.filter(Expense.title.ilike(f'%{search_query}%'))

    # Apply sorting
    sort_options = {
        'date_desc': Expense.date.desc(),
        'date_asc': Expense.date.asc(),
        'amount_desc': Expense.amount.desc(),
        'amount_asc': Expense.amount.asc(),
        'category': Expense.category.asc(),
    }
    sort_order = sort_options.get(sort_by, Expense.date.desc())
    expenses = query.order_by(sort_order).all()

    # Analytics on the full (unfiltered) data for charts
    all_expenses = Expense.query.filter_by(user_id=current_user.id).all()
    analytics = get_analytics(all_expenses)

    # Monthly summary for current month
    now = date.today()
    current_month_expenses = Expense.query.filter_by(user_id=current_user.id).filter(
        extract('year', Expense.date) == now.year,
        extract('month', Expense.date) == now.month,
    ).all()
    current_month_total = round(sum(e.amount for e in current_month_expenses), 2)

    # Budget for current month
    budget = Budget.query.filter_by(
        user_id=current_user.id, month=now.month, year=now.year
    ).first()
    budget_amount    = budget.amount if budget else None
    budget_pct       = round((current_month_total / budget_amount) * 100, 1) if budget_amount else None
    budget_remaining = round(budget_amount - current_month_total, 2) if budget_amount else None

    return render_template(
        'dashboard.html',
        expenses=expenses,
        analytics=analytics,
        categories=CATEGORIES,
        selected_category=selected_category,
        selected_month=selected_month,
        sort_by=sort_by,
        search_query=search_query,
        current_month_total=current_month_total,
        current_month=now.strftime('%B %Y'),
        now=now,
        budget_amount=budget_amount,
        budget_pct=budget_pct,
        budget_remaining=budget_remaining,
    )
