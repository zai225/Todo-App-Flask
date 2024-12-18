from flask import Flask, render_template, request, redirect
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy.sql import func

# basedir = os.path.abspath(os.path.dirname(_file_))
# app = Flask(_name_)
# app.config['SQLALCHEMY_DATABASE_URI'] =\
#         'sqlite:///' + os.path.join(basedir, 'database.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    # date_created = db.column(db.DateTime, server_default=datetime.now(timezone.utc))
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form["title"]
        desc = request.form["desc"]
        todo =Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()    

    query = request.args.get("q")
    if query:
        allTodo = Todo.query.filter(
            Todo.title.contains(query) | Todo.desc.contains(query)
        ).all()
    else:
        allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)
    # return "<p>Hello, World!</p>"

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)
    

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)