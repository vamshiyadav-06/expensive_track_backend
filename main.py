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
    allow_origins=["*"],  # change later after deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT")),
        ssl_disabled=False
    )

    return connection


# ==========================================
# HEALTH CHECK ROUTE
# ==========================================

@app.get("/")
def home():
    return {"message": "Expense Tracker API Running Successfully"}


# ==========================================
# ADD EXPENSE
# ==========================================

@app.post("/add_expense")
def add_expense(expense: dict):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        INSERT INTO expenses
        (category, amount, payment_method, expense_date, description)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            expense["category"],
            expense["amount"],
            expense["payment_method"],
            expense["expense_date"],
            expense["description"]
        )

        cursor.execute(query, values)
        conn.commit()

        return {"msg": "Expense added successfully"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()


# ==========================================
# VIEW ALL EXPENSES
# ==========================================

@app.get("/get_all_expenses")
def get_all_expenses():

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT * FROM expenses"

        cursor.execute(query)
        data = cursor.fetchall()

        return {"all_expenses": data}

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()


# ==========================================
# GET SINGLE EXPENSE
# ==========================================

@app.get("/get_single_expense/{expense_id}")
def get_single_expense(expense_id: int):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT * FROM expenses WHERE expense_id=%s"

        cursor.execute(query, (expense_id,))
        data = cursor.fetchone()

        return {"expense_data": data}

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()


# ==========================================
# UPDATE EXPENSE
# ==========================================

@app.put("/update_expense/{expense_id}")
def update_expense(
    expense_id: int,
    updated_expense: dict
):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
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
            updated_expense["category"],
            updated_expense["amount"],
            updated_expense["payment_method"],
            updated_expense["expense_date"],
            updated_expense["description"],
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
        cursor.close()
        conn.close()


# ==========================================
# DELETE EXPENSE
# ==========================================

@app.delete("/delete_expense/{expense_id}")
def delete_expense(expense_id: int):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        DELETE FROM expenses
        WHERE expense_id=%s
        """

        cursor.execute(query, (expense_id,))
        conn.commit()

        return {
            "msg":
            "Expense deleted successfully"
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()


# ==========================================
# SEARCH EXPENSE
# ==========================================

@app.get("/view_exp/{search_text}")
def search_expense(search_text: str):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
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

        return {"search_result": data}

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()


# ==========================================
# SORT EXPENSES
# ==========================================

@app.get("/sort_exp/{sort_column}/{sort_order}")
def sort_expenses(
    sort_column: str,
    sort_order: str
):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        column_mapping = {
            "Title": "description",
            "Amount": "amount",
            "Category": "category"
        }

        db_column = column_mapping.get(sort_column)

        if not db_column:
            return {"error": "Invalid column"}

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

        return {"sorted_expenses": data}

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()


# ==========================================
# FILTER EXPENSES
# ==========================================

@app.get("/filter_exp/{category}")
def filter_expense(category: str):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        SELECT * FROM expenses
        WHERE category=%s
        """

        cursor.execute(query, (category,))
        data = cursor.fetchall()

        return {"filtered_expenses": data}

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()


# ==========================================
# ANALYZE SPENDING
# ==========================================

@app.get("/analyze_spending")
def analyze_spending():

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

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
                float(total_spending[0] or 0)
            },
            "category_spending":
            final_data
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()