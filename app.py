from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
#Database config and filepath and assigning the sql framework(sqlite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#initialize database with the setting of my application
db = SQLAlchemy(app)

#setting a database class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        #create a variable that gets the form html tag to get the content from our form
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        #create the new task and store it in a database then redirect to te mainroute
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        #if by any chance there is and issue creating the new task the except will show a string
        except:
            return 'There was an issue adding your task'
    else:
        #this is gonna look all the content in the database and return all of it
        tasks = Todo.query.order_by(Todo.date_created).all()
        #flask class to assign a template that helps reuse html/css/js then task = task(passing it to our template)
        return render_template('index.html', tasks = tasks)
@app.route('/delete/<int:id>')
def delete(id):
    #gets the task to delete and if it doesnt exit it will sent a 404 error
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was and issue updating this task'
    else:
        return render_template('update.html', task = task)

if __name__ == '__main__':
    app.run(debug=True)
