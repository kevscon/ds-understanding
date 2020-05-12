# package imports
from flask import Flask, render_template, request, redirect
from config import Config
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create app object
app = Flask(__name__)
# app configuration settings; create sql database file
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config.from_object(Config)
# create database instance
db = SQLAlchemy(app)

# modify SQL class
class Todo(db.Model):
    # task ID
    id = db.Column(db.Integer, primary_key=True)
    # task description
    content = db.Column(db.String(200), nullable=False) # character limit; blank not allowed
    # task timestamp
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # text for task objects
    def __repr__(self):
        # task ID formatted for route variable
        return '<Task %r>' % self.id

# decorator to link function to homepage
@app.route('/', methods=['POST', 'GET']) # POST allows input from webpage
# function to run on homepage
def index():
    # POST: action if input submitted
    if request.method == 'POST':
        # retrieve content based on name assigned in html file
        task_content = request.form['content']
        # create model class instance
        new_task = Todo(content=task_content)

        # send input to database
        try:
            # add task to database session
            db.session.add(new_task)
            # commit task to database
            db.session.commit()
            # redirect browser to homepage
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    # update tasks in index.html file
    else:
        # assign all database contents to variable
        tasks = Todo.query.order_by(Todo.date_created).all() # sorted by timestamp
        # render homepage with tasks input
        return render_template('index.html', tasks=tasks)

# function to delete task
@app.route('/delete/<int:id>') # delete link for selected task
def delete(id):
    # get task based on ID or return 404 error
    task_to_delete = Todo.query.get_or_404(id)

    # delete task; update db; return to homepage
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting that task'

# function to update task
@app.route('/update/<int:id>', methods=['GET', 'POST']) # update link for selected task
def update(id):
    # get task based on ID or return 404 error
    task = Todo.query.get_or_404(id)
    # POST: action if update submitted
    if request.method == 'POST':
        # assign task content to input in textbox
        task.content = request.form['content']

        # update database; return to homepage
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    # task info for update.html file
    else:
        # render update page with task input
        return render_template('update.html', task=task)

# check if code is being run as a script (not an import)
if __name__ == "__main__":
    # run app
    app.run(debug=True) # option to return error descriptions
