from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import os

app = Flask(__name__)
db = SQLAlchemy(app)
manager = Manager(app)
tasks = []

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    date = db.Column(db.Text)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/delete/<i>/')
def delete(i):
    task = Task.query.get_or_404(i)
    if task is None:
        return redirect('/')
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/add', methods=['POST'])
def add():
    if request.methods == 'POST':
        message = request.form.get('message')
        date  = request.form.get('date')
        task = Task(message = message, date = date)
        db.session.add(task)

    return redirect('/')

@app.route('/edit/<i>/', methods=['GET','POST'])
def edit(i):
    if request.method == 'POST':
        task = Task.query.get_or_404(i)
        task.message = request.form.get('message')
        task.date = request.form.get('date')
        if task is None:
            return redirect('/')
        db.session.add(task)

        return redirect('/')
    else:
        task = Task.query.get_or_404(i)
        if task is None:
            return redirect('/')
        return render_template('tasks.html', task=task)



def main():
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    manager.run('localhost', 8000, debug=False)

if __name__ == '__main__':
    main()
