from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)



# Create a model/table
class Todo(db.Model): # Table name will be todo
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self): # This is the representation of the model
        return '<Task %r>' % self.id # This will show the id when we create a new task

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'] # This will get the content from the form
        new_task = Todo(content=task_content) # This will create a new task
        
        try:
            db.session.add(new_task) # This will add the new task to the database
            db.session.commit() # This will commit the changes to the database
            return redirect('/') # This will redirect to the index page
        except:
            return 'Error while adding the task'
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # This will get all the tasks from the database
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)  # This will get the task from the database
    
    try:
        db.session.delete(task_to_delete) # This will delete the task from the database
        db.session.commit() # This will commit the changes to the database
        return redirect('/') # This will redirect to the index page
    except:
        return 'Error while deleting the task'
    
    
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit() # This will commit the changes to the database
            return redirect('/') # This will redirect to the index page
        except:
            return 'Error while updating the task'
        
    else:
        return render_template('update.html', task=task)

if __name__ == '__main__':
    with app.app_context(): # This is to create the database
        db.create_all() # This will create the database
    app.run(debug=True)