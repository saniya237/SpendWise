from datetime import datetime
from database import connect

CATEGORIES = {"Food", "Transport", "Shopping", "Bills", "Education", "Health", "Entertainment", "Other"}

def validate(date, category, amount, description):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValueError("Please enter a valid date.")
    category = (category or "").strip()
    if category not in CATEGORIES:
        raise ValueError("Please choose a valid category.")
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a valid number.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return date, category, round(amount, 2), (description or "").strip()[:250]

def list_expenses(category="", start="", end=""):
    query, params = "SELECT * FROM expenses WHERE 1=1", []
    if category:
        query += " AND category=?"; params.append(category)
    if start:
        query += " AND date>=?"; params.append(start)
    if end:
        query += " AND date<=?"; params.append(end)
    query += " ORDER BY date DESC, id DESC"
    with connect() as db:
        rows = db.execute(query, params).fetchall()
    return [dict(r) for r in rows]

def get_expense(item_id):
    with connect() as db:
        row = db.execute("SELECT * FROM expenses WHERE id=?", (item_id,)).fetchone()
    return dict(row) if row else None

def create_expense(date, category, amount, description):
    values = validate(date, category, amount, description)
    with connect() as db:
        db.execute("INSERT INTO expenses(date,category,amount,description) VALUES(?,?,?,?)", values)

def update_expense(item_id, date, category, amount, description):
    values = validate(date, category, amount, description)
    with connect() as db:
        cur = db.execute("UPDATE expenses SET date=?,category=?,amount=?,description=? WHERE id=?",
                         (*values, item_id))
        return cur.rowcount > 0

def delete_expense(item_id):
    with connect() as db:
        cur = db.execute("DELETE FROM expenses WHERE id=?", (item_id,))
        return cur.rowcount > 0

def summary(rows):
    total = round(sum(float(r["amount"]) for r in rows), 2)
    grouped = {}
    for r in rows:
        grouped[r["category"]] = grouped.get(r["category"], 0) + float(r["amount"])
    return {"count": len(rows), "total": total,
            "average": round(total / len(rows), 2) if rows else 0,
            "categories": sorted(grouped.items(), key=lambda x: x[1], reverse=True)}
