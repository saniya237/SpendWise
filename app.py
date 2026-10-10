from flask import Flask, render_template, request, redirect, url_for, flash, Response
from pathlib import Path
import csv, io, logging
from database import init_db
from services import list_expenses, get_expense, create_expense, update_expense, delete_expense, summary

BASE = Path(__file__).resolve().parent
(BASE / "logs").mkdir(exist_ok=True)
logging.basicConfig(filename=BASE / "logs" / "app.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
app = Flask(__name__)
app.secret_key = "local-demo-key-change-before-deployment"
init_db()
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Education", "Health", "Entertainment", "Other"]

@app.get("/")
def index():
    category = request.args.get("category", "")
    start = request.args.get("start_date", "")
    end = request.args.get("end_date", "")
    expenses = list_expenses(category, start, end)
    return render_template("index.html", expenses=expenses, stats=summary(expenses),
                           categories=CATEGORIES, category=category, start=start, end=end)

@app.post("/expenses")
def add():
    try:
        create_expense(request.form.get("date", ""), request.form.get("category", ""),
                       request.form.get("amount", ""), request.form.get("description", ""))
        flash("Expense added successfully.", "success")
        logging.info("Expense added")
    except ValueError as exc:
        flash(str(exc), "error")
    except Exception:
        logging.exception("Expense creation failed")
        flash("Could not save this expense. Check the input and try again.", "error")
    return redirect(url_for("index"))

@app.get("/expenses/<int:item_id>/edit")
def edit_page(item_id):
    item = get_expense(item_id)
    if not item:
        flash("Expense not found.", "error")
        return redirect(url_for("index"))
    return render_template("edit.html", item=item, categories=CATEGORIES)

@app.post("/expenses/<int:item_id>/edit")
def edit(item_id):
    try:
        if not get_expense(item_id):
            flash("Expense not found.", "error")
        else:
            update_expense(item_id, request.form.get("date", ""), request.form.get("category", ""),
                           request.form.get("amount", ""), request.form.get("description", ""))
            flash("Expense updated.", "success")
            logging.info("Expense updated id=%s", item_id)
    except ValueError as exc:
        flash(str(exc), "error")
    except Exception:
        logging.exception("Expense update failed id=%s", item_id)
        flash("Could not update this expense.", "error")
    return redirect(url_for("index"))

@app.post("/expenses/<int:item_id>/delete")
def remove(item_id):
    try:
        deleted = delete_expense(item_id)
        flash("Expense deleted." if deleted else "Expense not found.", "success" if deleted else "error")
        logging.info("Delete requested id=%s", item_id)
    except Exception:
        logging.exception("Expense deletion failed id=%s", item_id)
        flash("Could not delete this expense.", "error")
    return redirect(url_for("index"))

@app.get("/export")
def export():
    rows = list_expenses(request.args.get("category", ""), request.args.get("start_date", ""),
                          request.args.get("end_date", ""))
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Category", "Amount", "Description"])
    for row in rows:
        writer.writerow([row["date"], row["category"], row["amount"], row["description"]])
    return Response(output.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=spendwise_expenses.csv"})

if __name__ == "__main__":
    app.run(debug=True)
