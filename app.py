from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import datetime

from models import db, User, Application, Interview, Contact

app = Flask(__name__, template_folder="templates")
app.secret_key = "supersecretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/applications', methods=['GET', 'POST'])
def applications():
    if request.method == 'POST':
        new_app = Application(
            company=request.form['company'],
            role=request.form['role'],
            status=request.form['status'],
            applied_date=datetime.datetime.strptime(request.form['applied_date'], "%Y-%m-%d"),
            follow_up_date=datetime.datetime.strptime(request.form['follow_up_date'], "%Y-%m-%d") if request.form['follow_up_date'] else None,
            notes=request.form['notes']
        )
        db.session.add(new_app)
        db.session.commit()
        flash("Application added successfully!")
        return redirect('/applications')

    applications = Application.query.all()
    return render_template('applications.html', applications=applications)

@app.route('/applications/edit/<int:id>', methods=['GET', 'POST'])
def edit_application(id):
    app_to_edit = Application.query.get_or_404(id)

    if request.method == 'POST':
        app_to_edit.company = request.form['company']
        app_to_edit.role = request.form['role']
        app_to_edit.status = request.form['status']
        app_to_edit.applied_date = datetime.datetime.strptime(request.form['applied_date'], "%Y-%m-%d")
        app_to_edit.follow_up_date = datetime.datetime.strptime(request.form['follow_up_date'], "%Y-%m-%d") if request.form['follow_up_date'] else None
        app_to_edit.notes = request.form['notes']

        db.session.commit()
        flash("Application updated.")
        return redirect('/applications')

    return render_template('edit_application.html', app=app_to_edit)

@app.route('/applications/delete/<int:id>', methods=['POST'])
def delete_application(id):
    app_to_delete = Application.query.get_or_404(id)
    db.session.delete(app_to_delete)
    db.session.commit()
    flash("Application deleted.")
    return redirect('/applications')

@app.route('/report')
def report():
    status = request.args.get('status')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    sql = "SELECT * FROM application WHERE 1=1"
    summary_sql = "SELECT status, COUNT(*) as count FROM application WHERE 1=1"
    params = {}
    summary_params = {}

    if status:
        sql += " AND status = :status"
        summary_sql += " AND status = :status"
        params['status'] = status
        summary_params['status'] = status
    if start_date and end_date:
        sql += " AND applied_date BETWEEN :start AND :end"
        summary_sql += " AND applied_date BETWEEN :start AND :end"
        params['start'] = start_date
        params['end'] = end_date
        summary_params['start'] = start_date
        summary_params['end'] = end_date

    results = db.session.execute(text(sql), params).fetchall()
    summary = db.session.execute(text(summary_sql + " GROUP BY status"), summary_params).fetchall()

    return render_template('report.html', results=results, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
