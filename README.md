# 💰 Personal Expense Tracker

A full-stack web application built with **Python & Flask** that helps users record, manage, and visually analyze their daily expenses.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.3-black?style=flat-square&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=flat-square&logo=sqlite)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=flat-square&logo=bootstrap)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4-red?style=flat-square&logo=chartdotjs)

---

## 📸 Screenshots

> Dashboard with charts, budget progress bar, and expense table.

| Login Page | Dashboard | Add Expense |
|---|---|---|
| Dark glassmorphism UI | Charts + Budget tracker | Clean form with validation |

---

## ✨ Features

- 🔐 **Secure Authentication** — Register, login, logout with hashed passwords (scrypt)
- 📝 **Expense CRUD** — Add, edit, delete expenses with full validation
- 🏷️ **12 Categories** — Food, Transport, Shopping, Bills, Entertainment and more
- 📊 **3 Charts** — Monthly trend (line), Category breakdown (doughnut), Top 5 (bar)
- 🎯 **Monthly Budget** — Set a budget, track progress with a color-coded bar and overspend alert
- 🔍 **Filter & Search** — Filter by category, month, keyword; sort by date or amount
- 📥 **CSV Export** — Download expenses as a CSV file (respects active filters)
- 💰 **INR Formatting** — Indian Rupee (₹) with proper comma system (1,00,000)
- 📱 **Responsive UI** — Bootstrap 5, works on mobile, tablet, and desktop
- ⚠️ **Custom Error Pages** — Styled 404, 500, 403 pages
- ✅ **Flash Messages** — Success, error, info alerts with auto-dismiss

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask 3.0 |
| Database | SQLite + SQLAlchemy ORM |
| Auth | Flask-Login + Werkzeug password hashing |
| Migrations | Flask-Migrate (Alembic) |
| Frontend | HTML5, Jinja2, Bootstrap 5.3 |
| Charts | Chart.js 4.4 |
| Icons | Bootstrap Icons 1.11 |
| Config | python-dotenv |
| Production | Gunicorn |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- pip

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/personal-expense-tracker.git
cd personal-expense-tracker
```

**2. Create and activate a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**
```bash
cp .env.example .env
```
Edit `.env` and set a strong `SECRET_KEY`:
```
SECRET_KEY=your-very-secret-key-here
DATABASE_URL=sqlite:///expenses.db
FLASK_APP=run.py
FLASK_ENV=development
```

**5. Run the application**
```bash
python run.py
```

Open your browser at **http://127.0.0.1:5000**

---

## 🌱 Load Demo Data

To populate the database with 40 realistic INR expenses and a demo account:

```bash
python seed_data.py
```

Login credentials:
```
Email:    demo@example.com
Password: demo1234
```

---

## 📁 Project Structure

```
personal-expense-tracker/
│
├── app/
│   ├── __init__.py          # App factory — Flask, SQLAlchemy, LoginManager
│   ├── models.py            # User, Expense, Budget models
│   ├── routes/
│   │   ├── auth.py          # Register, Login, Logout
│   │   ├── expenses.py      # Add, Edit, Delete expenses
│   │   ├── dashboard.py     # Dashboard + filters + analytics
│   │   └── budget.py        # Budget management + CSV export
│   ├── templates/
│   │   ├── base.html        # Base layout (navbar, flash messages)
│   │   ├── login.html       # Login page (glassmorphism UI)
│   │   ├── register.html    # Register page
│   │   ├── dashboard.html   # Main dashboard with charts
│   │   ├── expense_form.html# Add / Edit expense form
│   │   ├── budget.html      # Budget management page
│   │   └── errors/
│   │       ├── 404.html
│   │       ├── 500.html
│   │       └── 403.html
│   └── static/
│       └── css/
│           └── style.css    # Custom styles + glassmorphism
│
├── run.py                   # Entry point
├── seed_data.py             # Demo data seeder
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 📊 Database Models

### User
| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| username | String(80) | Unique username |
| email | String(120) | Unique email |
| password_hash | String(256) | Hashed password |
| created_at | DateTime | Account creation time |

### Expense
| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| title | String(120) | Expense title |
| amount | Float | Amount in ₹ |
| category | String(50) | One of 12 categories |
| date | Date | Expense date |
| notes | Text | Optional notes |
| user_id | FK → users | Owner |

### Budget
| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| user_id | FK → users | Owner |
| amount | Float | Monthly budget in ₹ |
| month | Integer | Month (1–12) |
| year | Integer | Year |

---

## 🌐 Routes

| Method | URL | Description |
|---|---|---|
| GET/POST | `/register` | User registration |
| GET/POST | `/login` | User login |
| GET | `/logout` | Logout |
| GET | `/` or `/dashboard` | Main dashboard |
| GET/POST | `/expenses/add` | Add expense |
| GET/POST | `/expenses/edit/<id>` | Edit expense |
| POST | `/expenses/delete/<id>` | Delete expense |
| GET | `/expenses/export` | Download CSV |
| GET/POST | `/budget` | Manage budgets |
| POST | `/budget/delete/<id>` | Delete a budget |

---

## 🚢 Deployment

### Deploy on Render (free tier)

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn run:app`
6. Add environment variables: `SECRET_KEY`, `DATABASE_URL`
7. Click **Deploy**

> For production, switch `DATABASE_URL` to a PostgreSQL URL (Render provides a free PostgreSQL instance).

---

## 🔮 Future Improvements

- [ ] Password reset via email
- [ ] PostgreSQL support for production
- [ ] Recurring expense tracking
- [ ] Export to PDF
- [ ] Income tracking and net balance
- [ ] Dark mode toggle
- [ ] GitHub Actions CI/CD pipeline

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

Built with ❤️ as a full-stack Python web development project.

> **"Empower users to gain control over their finances through a simple, secure, and visual expense tracker."**
