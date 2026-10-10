# SpendWise — Python Capstone Project

A portfolio-ready personal expense tracker built with Python, Flask and SQLite.

## Features
- Add, view, edit and delete expense records
- SQLite persistence
- Filter by category and date range
- Total, average and category-wise summaries
- CSV export
- Input validation and friendly error messages
- Application logging

## Run on Windows
```powershell
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`.

## Architecture
Browser → Flask routes (`app.py`) → validation/data operations (`services.py`) → SQLite (`database.py`) → HTML response or CSV download.

## Database schema
`expenses(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, category TEXT NOT NULL, amount REAL NOT NULL CHECK(amount > 0), description TEXT NOT NULL DEFAULT '')`

## Test checklist
1. Add an expense with a valid date and positive amount.
2. Try an invalid/negative amount.
3. Edit and delete an expense.
4. Filter by category and date.
5. Export the list to CSV.
6. Restart the app and check that records persist.
7. Inspect `logs/app.log` if needed.

## Demo video
Record a 1–3 minute screen recording showing adding, editing, filtering, summaries and CSV export. Add the video URL here if hosted.

## Deployment
Deployment is optional. Before deploying, use an environment variable for the Flask secret key, turn off debug mode and configure persistent database storage. The included secret key is for local demonstration only.
