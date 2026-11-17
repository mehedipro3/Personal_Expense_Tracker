# 💸 Personal Expense Tracker API

A personal income & expense tracker REST API built with **FastAPI**, **SQLAlchemy** and **PostgreSQL**, secured with **JWT authentication**. Every user can only see and manage their own transactions.

## 🌐 Live Demo
- **Live API:** https://personal-expense-tracker-7us1.onrender.com/
- **Swagger UI (try it here):** https://personal-expense-tracker-7us1.onrender.com/docs

> Hosted on Render's free plan, so the first request after a period of inactivity can take about 30–60 seconds while the service wakes up.

## ✨ Features
- User registration with bcrypt-hashed passwords (the hash is never returned)
- Login that returns a JWT access token
- Full CRUD for transactions, protected by JWT
- Per-user data isolation: users can never read, update or delete someone else's transactions
- Filtering by type, category, minimum and maximum amount
- Pydantic validation (amount must be positive, type must be `income` or `expense`)
- Pytest suite with 5 tests on an isolated in-memory database

## 🛠️ Tech Stack
FastAPI • SQLAlchemy • PostgreSQL • Pydantic • PyJWT • bcrypt • Pytest • Render

## 📂 Project Structure
```
Personal_Expense_Tracker/
├── main.py             # App entry point, router registration
├── database.py         # Engine, session, Base, get_db dependency
├── models.py           # User & Transaction SQLAlchemy models
├── schemas.py          # Pydantic request/response models
├── router/
│   ├── auth.py         # JWT + password helpers, /auth/register, /auth/login
│   └── transactions.py # /transactions CRUD + /transactions/filter
├── tests/
│   └── test_transactions.py
├── requirements.txt
├── .python-version     # Pins Python 3.12 for Render
└── .env.example
```

## 🔗 API Endpoints
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | ❌ | Register a new user |
| POST | `/auth/login` | ❌ | Login, returns `access_token` and `token_type` |
| POST | `/transactions` | ✅ | Create a transaction |
| GET | `/transactions` | ✅ | List my transactions |
| GET | `/transactions/filter` | ✅ | Filter my transactions |
| GET | `/transactions/{id}` | ✅ | Get one transaction |
| PUT | `/transactions/{id}` | ✅ | Update a transaction |
| DELETE | `/transactions/{id}` | ✅ | Delete a transaction |

**Filter example:**
`/transactions/filter?type=expense&category=Food&minimum_amount=100&maximum_amount=5000`

## 🚀 Quick Start (Live API)
1. Open https://personal-expense-tracker-7us1.onrender.com/docs
2. **Register:** `POST /auth/register`
   ```json
   { "username": "mehedi", "email": "mehedi@example.com", "password": "secret123" }
   ```
3. Click **Authorize** (top right), enter your username and password.
4. **Create a transaction:** `POST /transactions`
   ```json
   { "title": "Lunch", "amount": 250.5, "type": "expense", "category": "Food", "date": "2026-11-18" }
   ```
5. Try `GET /transactions`, `GET /transactions/filter?type=expense`, and so on.

Outside Swagger, send the token as a header: `Authorization: Bearer <access_token>`

## ⚙️ Run Locally
```bash
git clone https://github.com/mehedipro3/Personal_Expense_Tracker.git
cd Personal_Expense_Tracker
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then set DATABASE_URL and SECRET_KEY
uvicorn main:app --reload
```
Docs: http://127.0.0.1:8000/docs

If `DATABASE_URL` is not set, the app falls back to a local SQLite file so you can try it right away. Tables are created automatically on startup.

### Environment variables
| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Long random string used to sign JWTs |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime (default `60`) |

## 🧪 Run Tests
```bash
pytest -v
```
Covers: create, get all, get one, update and delete transaction.

## ☁️ Deployment (Render)
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment variables:** `DATABASE_URL`, `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- **Python version:** pinned to 3.12.8 through `.python-version`

## 👤 Author
**Mehedi** — [GitHub](https://github.com/mehedipro3)
