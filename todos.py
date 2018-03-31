from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////" + os.getcwd() + "/todos.db" 
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    isComplete = db.Column(db.Boolean)

@app.route("/")
def index():
    todos = Todo.query.all()

    return render_template("index.html", todos=todos)

@app.route("/activeTodos")
def activeTodos():
    todos = Todo.query.filter_by(isComplete="0")

    return render_template("index.html", todos=todos)

@app.route("/completeTodos")
def completeTodos():
    todos = Todo.query.filter_by(isComplete="1")

    return render_template("index.html", todos=todos)

@app.route("/addTodo", methods=["POST"])
def addTodo():
    todoTitle = request.form.get("title")
    todoContent = request.form.get("content")

    todo = Todo(title=todoTitle, content=todoContent, isComplete=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/completeTodo/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id=id).first()

    if(todo.isComplete == False):
        todo.isComplete = True
    else:
        todo.isComplete = False

    db.session.commit()

    return redirect(url_for("index"))


@app.route("/removeTodo/<string:id>")
def removeTodo(id):
    todo = Todo.query.filter_by(id=id).first()

    db.session.delete(todo)
    db.session.commit()
    
    return redirect(url_for("index"))

@app.route("/detailTodo/<string:id>", methods=["GET", "POST"])
def detailTodo(id):
    todo = Todo.query.filter_by(id=id).first()

    return render_template("detail.html", todo=todo)

if __name__ == "__main__":
    app.run(debug=True)