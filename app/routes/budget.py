import csv
import io
from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import login_required, current_user
from datetime import date
from sqlalchemy import extract
from app import db
from app.models import Budget, Expense, CATEGORIES

budget_bp = Blueprint('budget', __name__)


@budget_bp.route('/budget', methods=['GET', 'POST'])
@login_required
def set_budget():
    now = date.today()

    if request.method == 'POST':
        amount_str = request.form.get('amount', '').strip()
        month_str  = request.form.get('month', '').strip()  # YYYY-MM

        errors = []
        if not amount_str:
            errors.append('Budget amount is required.')
        else:
            try:
                amount = float(amount_str)
                if amount <= 0:
                    errors.append('Budget must be greater than zero.')
            except ValueError:
                errors.append('Budget must be a valid number.')
                amount = None

        if not month_str:
            errors.append('Month is required.')
        else:
            try:
                from datetime import datetime as dt
                parsed = dt.strptime(month_str, '%Y-%m')
                b_month, b_year = parsed.month, parsed.year
            except ValueError:
                errors.append('Invalid month format.')
                b_month = b_year = None

        if errors:
            for e in errors:
                flash(e, 'danger')
            return redirect(url_for('budget.set_budget'))

        # Upsert — update if exists, else create
        existing = Budget.query.filter_by(
            user_id=current_user.id, month=b_month, year=b_year
        ).first()

        try:
            if existing:
                existing.amount = amount
                existing.updated_at = dt.utcnow()
            else:
                db.session.add(Budget(
                    user_id=current_user.id,
                    amount=amount,
                    month=b_month,
                    year=b_year,
                ))
            db.session.commit()
            flash(f'Budget set to ₹{amount:,.2f} for {parsed.strftime("%B %Y")}.', 'success')
        except Exception:
            db.session.rollback()
            flash('Could not save budget. Please try again.', 'danger')

        return redirect(url_for('dashboard.index'))

    # GET — show budget management page
    budgets = (
        Budget.query
        .filter_by(user_id=current_user.id)
        .order_by(Budget.year.desc(), Budget.month.desc())
        .all()
    )
    return render_template('budget.html', budgets=budgets, now=now)


@budget_bp.route('/budget/delete/<int:budget_id>', methods=['POST'])
@login_required
def delete_budget(budget_id):
    b = db.session.get(Budget, budget_id)
    if b is None or b.user_id != current_user.id:
        flash('Budget not found.', 'danger')
        return redirect(url_for('budget.set_budget'))
    try:
        db.session.delete(b)
        db.session.commit()
        flash('Budget removed.', 'success')
    except Exception:
        db.session.rollback()
        flash('Could not delete budget.', 'danger')
    return redirect(url_for('budget.set_budget'))


# ── CSV Export ────────────────────────────────────────────────────────────────

@budget_bp.route('/expenses/export')
@login_required
def export_csv():
    """Download all expenses for the current user as a CSV file."""
    selected_category = request.args.get('category', '')
    selected_month    = request.args.get('month', '')

    query = Expense.query.filter_by(user_id=current_user.id)

    if selected_category and selected_category in CATEGORIES:
        query = query.filter(Expense.category == selected_category)

    if selected_month:
        try:
            from datetime import datetime as dt
            parsed = dt.strptime(selected_month, '%Y-%m')
            query = query.filter(
                extract('year',  Expense.date) == parsed.year,
                extract('month', Expense.date) == parsed.month,
            )
        except ValueError:
            pass

    expenses = query.order_by(Expense.date.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['#', 'Title', 'Amount (₹)', 'Category', 'Date', 'Notes'])
    for i, e in enumerate(expenses, 1):
        writer.writerow([
            i,
            e.title,
            f'{e.amount:.2f}',
            e.category,
            e.date.strftime('%d-%m-%Y'),
            e.notes or '',
        ])

    filename = f'expenses_{date.today().strftime("%Y%m%d")}.csv'
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'},
    )
