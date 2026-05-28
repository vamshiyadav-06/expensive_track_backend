from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os

app = FastAPI()

# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():

    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT")),
        ssl_disabled=True
    )


# ==========================================
# HEALTH CHECK ROUTE
# ==========================================

@app.get("/")
def home():
    return {
        "message":
        "Expense Tracker API Running Successfully"
    }


# ==========================================
# TEST DATABASE CONNECTION
# ==========================================

@app.get("/test_db")
def test_db():

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        return {
            "status": "success",
            "db": result,
            "host": os.getenv("DB_HOST"),
            "database": os.getenv("DB_NAME")
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==========================================
# ADD EXPENSE
# ==========================================

@app.post("/add_expense")
def add_expense(expense: dict):

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO expenses
        (
            category,
            amount,
            payment_method,
            expense_date,
            description
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            expense.get("category"),
            expense.get("amount"),
            expense.get("payment_method"),
            expense.get("expense_date"),
            expense.get("description")
        )

        cursor.execute(query, values)
        conn.commit()

        return {
            "msg":
            "Expense added successfully"
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==========================================
# VIEW ALL EXPENSES
# ==========================================

@app.get("/get_all_expenses")
def get_all_expenses():

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM expenses"

        cursor.execute(query)
        data = cursor.fetchall()

        return {
            "all_expenses": data
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==========================================
# GET SINGLE EXPENSE
# ==========================================

@app.get("/get_single_expense/{expense_id}")
def get_single_expense(expense_id: int):

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT * FROM expenses
        WHERE expense_id=%s
        """

        cursor.execute(
            query,
            (expense_id,)
        )

        data = cursor.fetchone()

        return {
            "expense_data": data
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==========================================
# UPDATE EXPENSE
# ==========================================

@app.put("/update_expense/{expense_id}")
def update_expense(
    expense_id: int,
    updated_expense: dict
):

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        UPDATE expenses
        SET category=%s,
            amount=%s,
            payment_method=%s,
            expense_date=%s,
            description=%s
        WHERE expense_id=%s
        """

        values = (
            updated_expense.get("category"),
            updated_expense.get("amount"),
            updated_expense.get(
                "payment_method"
            ),
            updated_expense.get(
                "expense_date"
            ),
            updated_expense.get(
                "description"
            ),
            expense_id
        )

        cursor.execute(query, values)
        conn.commit()

        return {
            "updated_msg":
            "Expense updated successfully"
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==========================================
# DELETE EXPENSE
# ==========================================

@app.delete("/delete_expense/{expense_id}")
def delete_expense(expense_id: int):

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        DELETE FROM expenses
        WHERE expense_id=%s
        """

        cursor.execute(
            query,
            (expense_id,)
        )

        conn.commit()

        return {
            "msg":
            "Expense deleted successfully"
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==========================================
# SEARCH EXPENSE
# ==========================================

@app.get("/view_exp/{search_text}")
def search_expense(search_text: str):

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT * FROM expenses
        WHERE category LIKE %s
        OR description LIKE %s
        """

        search = f"%{search_text}%"

        cursor.execute(
            query,
            (search, search)
        )

        data = cursor.fetchall()

        return {
            "search_result": data
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==========================================
# SORT EXPENSES
# ==========================================

@app.get("/sort_exp/{sort_column}/{sort_order}")
def sort_expenses(
    sort_column: str,
    sort_order: str
):

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        column_mapping = {
            "Title": "description",
            "Amount": "amount",
            "Category": "category"
        }

        db_column = column_mapping.get(
            sort_column
        )

        if not db_column:
            return {
                "error":
                "Invalid column"
            }

        order = (
            "ASC"
            if sort_order == "Asc"
            else "DESC"
        )

        query = f"""
        SELECT * FROM expenses
        ORDER BY {db_column} {order}
        """

        cursor.execute(query)

        data = cursor.fetchall()

        return {
            "sorted_expenses": data
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==========================================
# FILTER EXPENSES
# ==========================================

@app.get("/filter_exp/{category}")
def filter_expense(category: str):

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT * FROM expenses
        WHERE category=%s
        """

        cursor.execute(
            query,
            (category,)
        )

        data = cursor.fetchall()

        return {
            "filtered_expenses": data
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==========================================
# ANALYZE SPENDING
# ==========================================

@app.get("/analyze_spending")
def analyze_spending():

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT SUM(amount) FROM expenses"
        )

        total_spending = cursor.fetchone()

        cursor.execute("""
        SELECT category,
        SUM(amount)
        FROM expenses
        GROUP BY category
        """)

        category_spending = cursor.fetchall()

        final_data = []

        for row in category_spending:
            final_data.append({
                "category": row[0],
                "total": float(row[1])
            })

        return {
            "total_spending": {
                "total":
                float(
                    total_spending[0] or 0
                )
            },
            "category_spending":
            final_data
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()