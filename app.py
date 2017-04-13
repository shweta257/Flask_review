from flask import Flask, render_template, redirect, request, Response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user
import os, sys


app = Flask(__name__)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
manager = Manager(app)

app.config['SECRET_KEY'] = 'FLASK EXAMPLE'


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_pass"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


users = [User(id) for id in range(1, 2)]


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    date = db.Column(db.Text)

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_pass":
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            return redirect('/')
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')

@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username,password = token.split(":") # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user
    return None

@app.route('/')
@login_required
def index():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/delete/<i>/')
@login_required
def delete(i):
    task = Task.query.get_or_404(i)
    if task is None:
        return redirect('/')
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/add/', methods=['POST'])
@login_required
def add():
    if request.method == 'POST':
        message = request.form.get('message')
        date  = request.form.get('date')
        task = Task(message = message, date = date)
        db.session.add(task)

    return redirect('/')

@app.route('/edit/<i>/', methods=['GET','POST'])
@login_required
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
        return render_template('task_edit.html', task=task)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login/')

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

@login_manager.user_loader
def load_user(userid):
    return User(userid)

if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    if len(sys.argv) >= 2 and sys.argv[1] == 'init':
        db.create_all()
        db.session.commit()
        task = Task(message="This is my first task",date="04/04/2017")
        db.session.add(task)
        db.session.commit()
    app.run('localhost', 8000, debug=True)
