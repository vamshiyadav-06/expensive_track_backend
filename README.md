# 💰 Expense Management System

> A full-stack expense tracking application built with **FastAPI** (Python) backend and **Streamlit** frontend, backed by a **MySQL** database. Designed to help users log, view, search, delete, and analyze their personal expenses through a clean web interface.

---

## 📌 Project Overview

The **Expense Management System** is a full-stack web application that enables users to manage their daily expenses efficiently. The backend exposes a RESTful API built with FastAPI, while the frontend is a user-friendly Streamlit dashboard. All expense data is persisted in a MySQL database, with the backend and frontend communicating via HTTP requests.

This project demonstrates end-to-end application development — from database design and API development to frontend integration and cloud deployment.

---

## ✨ Features

- ➕ **Add Expenses** — Log new expenses with category, amount, payment method, date, and description
- 📋 **View All Expenses** — Retrieve and display all recorded expenses in a tabular format
- 🗑️ **Delete Expense** — Remove a specific expense record by its unique ID
- 🔍 **Search Expenses** — Search expenses by category or description using partial text matching
- 📈 **Analyze Spending** — View total spending and a per-category breakdown with interactive bar and pie charts
- 🔗 **Health Check** — Verify API availability
- 🛠️ **Database Test** — Check live database connectivity via a dedicated endpoint

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | FastAPI (Python) |
| **Frontend Framework** | Streamlit (Python) |
| **Database** | MySQL |
| **Database Driver** | `mysql-connector-python` |
| **Data Visualization** | Plotly Express |
| **Data Manipulation** | Pandas |
| **HTTP Client** | Requests |
| **Server** | Uvicorn (ASGI) |
| **Environment Config** | `python-dotenv` |
| **Deployment** | Render (Backend) / Streamlit Cloud (Frontend) |

---

## 🏗️ Architecture / Workflow

```
┌─────────────────────────┐         HTTP Requests        ┌──────────────────────────┐
│                         │  ─────────────────────────►  │                          │
│   Streamlit Frontend    │                               │   FastAPI Backend        │
│      (app.py)           │  ◄─────────────────────────  │      (main.py)           │
│                         │         JSON Responses        │                          │
└─────────────────────────┘                               └────────────┬─────────────┘
                                                                       │
                                                                       │ mysql-connector-python
                                                                       ▼
                                                          ┌──────────────────────────┐
                                                          │      MySQL Database       │
                                                          │    (expenses table)       │
                                                          └──────────────────────────┘
```

**Request Flow:**
1. User interacts with the Streamlit UI (selects operation, fills form)
2. Streamlit calls `make_request()` which sends an HTTP request to the FastAPI backend
3. FastAPI receives the request, opens a MySQL connection via `get_db_connection()`
4. The query is executed; results are returned as JSON
5. Streamlit renders the response — as a table, success message, or Plotly chart

---

## 📁 Project Structure

```
expense-tracker/
│
├── backend/
│   ├── main.py               # FastAPI app — all API routes and DB logic
│   └── requirements.txt      # Backend dependencies
│
├── frontend/
│   ├── app.py                # Streamlit UI — all pages and API calls
│   ├── requirements.txt      # Frontend dependencies
│   └── .streamlit/
│       └── secrets.toml      # Streamlit secrets (server_url)
│
└── README.md
```

> **Note:** Both `main.py` and `app.py` can be kept in the same repo or deployed separately.

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8+
- MySQL Server (local or cloud)
- `pip` package manager

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
```

---

## 🔧 Backend Setup

```bash
# Navigate to backend folder
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**`requirements.txt` (Backend)**
```
fastapi
uvicorn
mysql-connector-python
python-dotenv
```

### Run the Backend Server

```bash
uvicorn main:app --reload
```

Backend will be live at: `http://127.0.0.1:8000`

---

## 🎨 Frontend Setup

```bash
# Navigate to frontend folder
cd frontend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**`requirements.txt` (Frontend)**
```
streamlit
requests
pandas
plotly
```

### Configure Streamlit Secrets

Create the file `.streamlit/secrets.toml` in the frontend directory:

```toml
server_url = "http://127.0.0.1:8000"
```

> For production, replace with your deployed backend URL (e.g., Render URL).

### Run the Frontend

```bash
streamlit run app.py
```

Frontend will be live at: `http://localhost:8501`

---

## 🔐 Environment Variables

The backend reads all database credentials from environment variables. Create a `.env` file in the backend directory:

```env
DB_HOST=your_mysql_host
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
DB_PORT=3306
```

> `python-dotenv` will automatically load these variables when the server starts.

| Variable | Description | Example |
|---|---|---|
| `DB_HOST` | MySQL host address | `localhost` or cloud host |
| `DB_USER` | MySQL username | `root` |
| `DB_PASSWORD` | MySQL password | `yourpassword` |
| `DB_NAME` | Target database name | `expense_db` |
| `DB_PORT` | MySQL port | `3306` |

---

## 🗄️ Database Setup

### Step 1 — Create the Database

Log in to your MySQL server and run:

```sql
CREATE DATABASE expense_db;
```

### Step 2 — Create the Table

You can either hit the `/create_table` API endpoint after starting the server, or run this SQL manually:

```sql
CREATE TABLE IF NOT EXISTS expenses (
    expense_id      INT AUTO_INCREMENT PRIMARY KEY,
    category        VARCHAR(100),
    amount          DECIMAL(10, 2),
    payment_method  VARCHAR(100),
    expense_date    DATE,
    description     TEXT
);
```

### Step 3 — Verify via API

```
GET /test_db
```

Expected response:
```json
{
  "status": "success",
  "db": [1],
  "host": "your_host",
  "database": "expense_db"
}
```

---

## 📡 API Endpoints

| Method | Endpoint | Description | Request Body |
|---|---|---|---|
| `GET` | `/` | Health check — confirms API is running | — |
| `GET` | `/test_db` | Tests live database connection | — |
| `GET` | `/create_table` | Creates the `expenses` table if it doesn't exist | — |
| `POST` | `/add_expense` | Adds a new expense record | JSON (see below) |
| `GET` | `/get_all_expenses` | Returns all expense records | — |
| `GET` | `/get_single_expense/{expense_id}` | Returns one expense by ID | — |
| `PUT` | `/update_expense/{expense_id}` | Updates an existing expense by ID | JSON (see below) |
| `DELETE` | `/delete_expense/{expense_id}` | Deletes an expense by ID | — |
| `GET` | `/view_exp/{search_text}` | Searches expenses by category or description | — |
| `GET` | `/analyze_spending` | Returns total and per-category spending | — |

### Request Body — Add / Update Expense

```json
{
  "category": "Food",
  "amount": 250.00,
  "payment_method": "UPI",
  "expense_date": "2025-05-28",
  "description": "Lunch at café"
}
```

### Sample Analyze Response

```json
{
  "total_spending": { "total": 4500.00 },
  "category_spending": [
    { "category": "Food", "total": 1500.00 },
    { "category": "Travel", "total": 3000.00 }
  ]
}
```

---

## 🚀 Deployment

### Backend — Render

1. Push your backend code to a GitHub repository
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo
4. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`
5. Add all environment variables (`DB_HOST`, `DB_USER`, etc.) under **Environment**
6. Deploy — copy the generated Render URL

### Frontend — Streamlit Cloud

1. Push your frontend code to a GitHub repository
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) → **New App**
3. Connect your GitHub repo and select `app.py`
4. Under **Advanced Settings → Secrets**, add:
   ```toml
   server_url = "https://your-render-backend-url.onrender.com"
   ```
5. Deploy

---


## 🚧 Challenges Faced

- **CORS Configuration:** Enabling cross-origin requests between the Streamlit frontend and FastAPI backend required setting up `CORSMiddleware` correctly.
- **Database Connection Management:** Ensuring MySQL connections and cursors are always closed properly (using `finally` blocks) to prevent connection leaks.
- **Render Cold Starts:** The free tier of Render spins down idle services, causing the first request after inactivity to time out. Handled with a 60-second timeout and a user-facing warning in the UI.
- **Environment Variable Handling:** Safely reading DB credentials via `os.getenv()` and keeping secrets out of source code using `.env` and Streamlit Secrets.
- **Data Type Conversion:** MySQL `DECIMAL` values must be explicitly cast to `float` before returning in JSON to avoid serialization errors.

---

## 📚 Learnings

- Building and structuring a **RESTful API** with FastAPI, including path parameters, request bodies, and HTTP methods
- Connecting Python applications to **MySQL** using `mysql-connector-python` and writing parameterized queries to prevent SQL injection
- Designing a **Streamlit multi-page UI** using sidebar navigation and forms
- Creating **interactive data visualizations** (bar charts, pie charts) with Plotly Express
- Managing **environment variables** and application secrets across local and cloud environments
- End-to-end **deployment workflow** using Render and Streamlit Cloud
- Importance of proper **resource cleanup** (closing DB cursors and connections) in web APIs

---

## 🔮 Future Enhancements

- [ ] **User Authentication** — Add login/signup with JWT-based auth so each user sees only their own expenses
- [ ] **Update Expense UI** — The `PUT /update_expense` endpoint exists in the backend but is not yet wired to the frontend
- [ ] **Date Range Filtering** — Filter expenses by a start and end date in the View and Analyze screens
- [ ] **Monthly Trends Chart** — Visualize spending over time with a line chart grouped by month
- [ ] **Export to CSV** — Let users download their expense data as a CSV file
- [ ] **Budget Alerts** — Set spending limits per category and highlight when they are exceeded
- [ ] **Pagination** — Add pagination to the View Expenses table for large datasets
- [ ] **Input Validation** — Add stricter backend validation using Pydantic models instead of raw `dict`
- [ ] **Docker Support** — Containerize both services with Docker Compose for easier local setup

---

## 👨‍💻 Author

**Budida Vamshi**
- GitHub: [@vamshiyadav-06](https://github.com/vamshiyadav-06)
- LinkedIn: [Budida Vamshi](https://www.linkedin.com/in/budida-vamshi-22b622312)
- Email: vanshiyadav245@gmail.com

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

> ⭐ If you found this project helpful, please consider giving it a star on GitHub!
