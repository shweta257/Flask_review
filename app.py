from flask import Flask, render_template, redirect
app = Flask(__name__)

tasks = []
@app.route('/')
def index():
    return render_template('tasks.html', tasks=tasks)

@app.route('/delete/<i>/')
def delete(i):
    del tasks[int(i)]
    return redirect('/')

def main():
    tasks.append('task 1')
    tasks.append('task 2')
    app.run('localhost', 8000, debug=False)

if __name__ == '__main__':
    main()
