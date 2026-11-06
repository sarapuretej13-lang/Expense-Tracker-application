from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from datetime import datetime, date
from app import db
from app.models import Expense, CATEGORIES

expenses_bp = Blueprint('expenses', __name__)


def parse_date(date_str):
    """Parse date string to date object, return today on failure."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return date.today()


@expenses_bp.route('/expenses/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        amount_str = request.form.get('amount', '').strip()
        category = request.form.get('category', '').strip()
        date_str = request.form.get('date', '').strip()
        notes = request.form.get('notes', '').strip()

        errors = []
        if not title or len(title) < 2:
            errors.append('Title must be at least 2 characters.')
        if not amount_str:
            errors.append('Amount is required.')
        else:
            try:
                amount = float(amount_str)
                if amount <= 0:
                    errors.append('Amount must be greater than zero.')
            except ValueError:
                errors.append('Amount must be a valid number.')
                amount = None
        if not category or category not in CATEGORIES:
            errors.append('Please select a valid category.')
        if not date_str:
            errors.append('Date is required.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template(
                'expense_form.html',
                categories=CATEGORIES,
                form_data=request.form,
                action='Add',
            )

        try:
            expense = Expense(
                title=title,
                amount=float(amount_str),
                category=category,
                date=parse_date(date_str),
                notes=notes if notes else None,
                user_id=current_user.id,
            )
            db.session.add(expense)
            db.session.commit()
            flash(f'Expense "{title}" added successfully!', 'success')
            return redirect(url_for('dashboard.index'))
        except Exception:
            db.session.rollback()
            flash('An error occurred while saving. Please try again.', 'danger')

    return render_template(
        'expense_form.html',
        categories=CATEGORIES,
        form_data={'date': date.today().strftime('%Y-%m-%d')},
        action='Add',
    )


@expenses_bp.route('/expenses/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = db.session.get(Expense, expense_id)
    if expense is None:
        abort(404)

    # Ensure the expense belongs to the current user
    if expense.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        amount_str = request.form.get('amount', '').strip()
        category = request.form.get('category', '').strip()
        date_str = request.form.get('date', '').strip()
        notes = request.form.get('notes', '').strip()

        errors = []
        if not title or len(title) < 2:
            errors.append('Title must be at least 2 characters.')
        if not amount_str:
            errors.append('Amount is required.')
        else:
            try:
                amount = float(amount_str)
                if amount <= 0:
                    errors.append('Amount must be greater than zero.')
            except ValueError:
                errors.append('Amount must be a valid number.')
        if not category or category not in CATEGORIES:
            errors.append('Please select a valid category.')
        if not date_str:
            errors.append('Date is required.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template(
                'expense_form.html',
                categories=CATEGORIES,
                form_data=request.form,
                action='Edit',
                expense=expense,
            )

        try:
            expense.title = title
            expense.amount = float(amount_str)
            expense.category = category
            expense.date = parse_date(date_str)
            expense.notes = notes if notes else None
            expense.updated_at = datetime.utcnow()
            db.session.commit()
            flash(f'Expense "{title}" updated successfully!', 'success')
            return redirect(url_for('dashboard.index'))
        except Exception:
            db.session.rollback()
            flash('An error occurred while updating. Please try again.', 'danger')

    return render_template(
        'expense_form.html',
        categories=CATEGORIES,
        form_data={
            'title': expense.title,
            'amount': expense.amount,
            'category': expense.category,
            'date': expense.date.strftime('%Y-%m-%d'),
            'notes': expense.notes or '',
        },
        action='Edit',
        expense=expense,
    )


@expenses_bp.route('/expenses/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = db.session.get(Expense, expense_id)
    if expense is None:
        abort(404)

    if expense.user_id != current_user.id:
        abort(403)

    try:
        title = expense.title
        db.session.delete(expense)
        db.session.commit()
        flash(f'Expense "{title}" deleted successfully.', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred while deleting. Please try again.', 'danger')

    return redirect(url_for('dashboard.index'))
