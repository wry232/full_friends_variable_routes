from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')

@app.route('/', methods=["post", "get"])
def index():
    query = "SELECT * FROM friends"
    friends = mysql.query_db(query)
    return render_template('index.html', all_friends=friends)

@app.route('/friends', methods=['post'])
def add():
    addUserData = {"first_name":request.form["first_name"], "last_name":request.form["last_name"], "email":request.form["email"]}
    query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
    mysql.query_db(query, addUserData)
    return redirect('/')

@app.route('/update/<id>/edit', methods=["post"])
def update_page(id):
    query = "SELECT * FROM friends WHERE id = :specific_id"
    data = {'specific_id': id}
    recordToUpdate = mysql.query_db(query, data)
    return render_template('update.html', recordToUpdate=recordToUpdate[0])

@app.route("/friends/<id>", methods=["post"])
def update_record(id):
    updateData = {"first_name":request.form["first_name"], "last_name":request.form["last_name"], "email":request.form["email"], "id":id}
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, email = :email WHERE id = :id"
    mysql.query_db(query, updateData)
    return redirect("/")

@app.route('/friends/<id>/delete', methods=["post"])
def delete(id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {"id": id}
    mysql.query_db(query, data)
    return redirect("/")

@app.route("/deleteConfirmation", methods=["post"])
def deleteConfirmation():
    idToDelete = request.form["id"]
    return render_template("confirm_delete.html", idToDelete=idToDelete)

app.run(debug=True)
