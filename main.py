from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import json
import os
from werkzeug.utils import secure_filename
import math
import random


app = Flask(__name__, template_folder='template')
app.secret_key = "akash-bayas-bais"

with open("configg.json", "r") as i:
    devil = json.load(i)["devil"]
app.config['upload'] = devil['docs_data']
def read_file(filename):
    with open(filename, 'rb') as f:
        photo = f.read()
    return photo

@app.route("/", methods=['GET','POST'])
def home():
    conn = mysql.connector.connect(host='localhost',
                                   user='root',
                                   password='',
                                   database='students')
    mycursor = conn.cursor()
    if request.method == 'POST':
        username = request.form["name"]
        coll = request.form["cname"]
        edu = request.form["edu"]
        expl = request.form["yedu"]
        mail = request.form["mail"]
        file = request.files["file1"]
        # a = file.filename
        # data = read_file(file)
        file.save(os.path.join(app.config['upload'], secure_filename(file.filename)))
        # return data
        sqlQuery = "INSERT INTO `student_table`(`Name`, `Collage`, `Education`, `Edu year`, `mail`) VALUES (%s, %s, %s, %s, %s)"
        mycursor.execute(sqlQuery, (username, coll, edu, expl, mail))
    conn.commit()
    mycursor.close()
    return render_template("index.html", devil=devil)

@app.route("/addd", methods=["GET","POST"])
def addd():
    conn = mysql.connector.connect(host='localhost',
                                   user='root',
                                   password='',
                                   database='students')
    mycursor = conn.cursor()

    query = "SELECT * FROM student_table"
    mycursor.execute(query)
    ndata = mycursor.fetchall()
    tmp = []
    for a in range(len(ndata)):
        t = ndata[a]
        tmp.append(t)

    if ('user' in session and session['user'] == devil['usrnm']):
        return render_template("dashboard.html", devil=devil, user=tmp)

    if request.method == "POST":
        usern = request.form["RUBY"]
        passw = request.form["SHELL"]

        if (usern == devil['usrnm'] and passw == devil['pswrd']):
            session['user'] = usern
            return render_template("dashboard.html", devil=devil, user=tmp)
    return render_template("addd.html", devil=devil)


@app.route("/logout")
def logoutt():
    session.pop('user')
    return redirect("/addd")


if __name__ == "__main__":
    app.run(debug=True)