#!/usr/bin/env python3
"""
Devon Kay
5-1-2025
I created this program on my own, using the readings as references, as well as one additional page
listed below
https://stackoverflow.com/questions/4710067/how-to-delete-a-specific-line-in-a-text-file-using-python
This was for modifying existing files
Aside from the dateformat filter, all of the code here was written by me
"""

from flask import Flask, render_template, request, redirect
import time
import string
import re
from datetime import datetime


def gettasks():
    tasks = r'^(\d+)\s(?!x\s)(\d+)\s(.*)' #regex for pending tasks
    completed = r'(\d+)\sx\s(\d+)\s(\d+)\s(.*)' #regex for completed tasks
    inprog = []
    overdue = []
    finished = []
    now = int(time.time()) #current time
    with open("todo.txt", "r") as f:
        for line in f:
            tasklist = re.findall(tasks, line, re.VERBOSE)
            complist = re.findall(completed, line, re.VERBOSE)
            for task in tasklist:
                if int(task[1]) > now: #if the duedate hasn't passed yet
                    inprog.append(task) #put it in inprog
                else:
                    overdue.append(task) #put it in overdue
            for comp in complist:
                finished.append(comp)
    return inprog, overdue, finished

app = Flask(__name__)

@app.template_filter('dateformat')
def format_date(timestamp):
    """Borrowed from assignment page: Converts a Unix timestamp to a more readable date format."""
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')

@app.route("/")
def index():
    inprog, overdue, finished = gettasks()
    return render_template("home.html", inprog=inprog, overdue=overdue,finished=finished)

@app.route("/add", methods = ["POST"])
def add():
    if request.method == 'POST':
        now = int(time.time())
        date = request.form.get('date')
        dt = datetime.strptime(date, "%Y-%m-%d")
        duedate = int(dt.timestamp())
        newTask = request.form.get('newTask')
        with open('todo.txt', 'a') as f: #add to existing file
            f.write(f"{now} {duedate} {newTask}\n")
    return redirect("/")

@app.route("/mark_complete/<task_id>", methods = ["GET"])
def mark_complete(task_id):
    inprog, overdue, finished = gettasks()
    now = int(time.time())
    with open("todo.txt", "w") as f:
        for task in inprog:
            if int(task[0]) == int(task_id): #if task_id equals creation timestamp
                f.write(f"{task[0]} x {now} {task[1]} {task[2]}\n") #mark it as complete
            else:
                f.write(f"{task[0]} {task[1]} {task[2]}\n") #otherwise, write it like normal
        for task1 in overdue:
            if int(task1[0]) == int(task_id): #if task_id equals creation timestamp
                f.write(f"{task1[0]} x {now} {task1[1]} {task1[2]}\n") #mark it as complete
            else:
                f.write(f"{task1[0]} {task1[1]} {task1[2]}\n")
        for task2 in finished:
            f.write(f"{task2[0]} x {task2[1]} {task2[2]} {task2[3]}\n") #nothing changes here
    return redirect("/")

@app.route("/delete_task/<task_id>", methods = ["GET"])
def deletetask(task_id):
    inprog, overdue, finished = gettasks()
    now = int(time.time())
    with open("todo.txt", "w") as f: #overwrite the existing file
        for task in inprog:
            if int(task[0]) != int(task_id): #as long as creation timestamp doesn't equal task_id
                f.write(f"{task[0]} {task[1]} {task[2]}\n") #write it to the new file
        for task in overdue:
            if int(task[0]) != int(task_id):
                f.write(f"{task[0]} {task[1]} {task[2]}\n")
        for task in finished:
            if int(task[0]) != int(task_id):
                f.write(f"{task[0]} x {task[1]} {task[2]} {task[3]}\n")
    return redirect("/")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html" ), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html",),500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11596)
