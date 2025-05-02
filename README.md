#  Application Tracker

This is a Flask-based job application tracker built for CS348. Users can add, edit, and track job applications and generate reports with filters.

## Features
- Add, update, and delete job applications
- Filtered reports by status and date
- Dynamic UI with database-driven content
- ORM and prepared SQL statements used
- Indexed fields for performance

## Demo
[Link to demo video] (if hosted)

## Project Structure
- `app.py` - Flask routes and application logic
- `models.py` - SQLAlchemy models and table schema
- `templates/` - HTML templates for UI
- `static/` - CSS styles

## Setup
```bash
pip install -r requirements.txt
python app.py
