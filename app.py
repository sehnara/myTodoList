from sre_constants import SUCCESS
from flask import Flask, render_template, request, jsonify
from itsdangerous import json
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbtodo

app = Flask('__name__')


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/todo/read")
def on_read():
    todos = list(db.todos.find({}, {'_id': False}))
    return jsonify({"result": "success", "todos": todos})


@app.route("/todo/write", methods=['POST'])
def on_write():
    title = request.form['title']
    contents = request.form['contents']
    startTime = request.form['startTime']
    endTime = request.form['endTime']
    ext = request.form['ext']
    importance = request.form['importance']
    success = request.form['success']

    todo = {
        'title': title,
        'contents': contents,
        'startTime': startTime,
        'endTime': endTime,
        'ext': ext,
        'importance': importance,
        'success': success
    }
    db.todos.insert_one(todo)
    return jsonify({"result": "success"})


@app.route("/todo/delete", methods=['POST'])
def on_delete():
    title = request.form['title']
    db.todos.delete_one({'title': title})
    return jsonify({"result": "success"})


@app.route("/todo/complete", methods=['POST'])
def on_complete():
    title = request.form['title']
    success = db.todos.find_one({'title': title})['success']
    db.todos.update_one({'title': title}, {'$set': {'success': not success}})
    return jsonify({"result": "success"})


if(__name__ == '__main__'):
    app.run('0.0.0.0', port=5000, debug=True)
