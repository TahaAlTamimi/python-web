# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 06:15:43 2019

@author: OJO3
"""

from flask import Flask,render_template,request, redirect, url_for
import sqlite3 as sql


app=Flask(__name__)
app.secret_key='abc'


@app.route('/')
def login():
    return render_template('login_project4.html')


@app.route('/login', methods=['POST','GET'])
def auth():
    if request.method == 'POST':
        try:
            username=request.form['username']
            password=request.form['password']
            with sql.connect("Org.db") as con:
                    cur = con.cursor()
                    cur.execute("select * from login WHERE username=? AND password=?",(username,password))
                    rows=cur.fetchall()
                    if len(rows):
                        print(rows)
                        return redirect(url_for('home'))
                    else:
                        return render_template('result_project4.html',msg="Username or Password is wrong")
        except:
            return render_template('result_project4.html',msg="Something went wrong")
        
    con.close()


@app.route('/home')
def home():
    return render_template('home_project4.html')


@app.route('/home/derpartments')
def departments_list():
    con = sql.connect("Org.db")
    con.row_factory = sql.Row
    
    cur= con.cursor()
    cur.execute("select * from departments")
    
    rows=cur.fetchall()
    print(rows)
    return render_template('departments_project4.html',rows=rows)


@app.route('/home/adddepartment', methods=['POST','GET'])
def add():
    if request.method == 'GET':
        return render_template('addDepartment_project4.html')
    
    if request.method == 'POST':
        department_name=request.form['name']
        location_id=request.form['location']
        with sql.connect("Org.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO departments (department_name,location_id)VALUES(?,?)",(department_name,location_id))
            con.commit()
            return redirect(url_for('departments_list'))


@app.route('/logout')
def logout():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run() 