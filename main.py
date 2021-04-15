from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import json
import math
import random


app = Flask(__name__, template_folder='template')
app.secret_key = "akash-bayas-bais"

with open("configg.json", "r") as i:
    devil = json.load(i)["devil"]

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
        sqlQuery = "INSERT INTO `student_table`(`Name`, `Collage`, `Education`, `Edu year`) VALUES (%s, %s, %s, %s)"
        mycursor.execute(sqlQuery, (username, coll, edu, expl))
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