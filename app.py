from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId

import os

host = os.environ.get("DB_URL")
client = MongoClient(host=host)
db = client.CharityTracker

#RESOURCES
users = db.users
donations = db.donations

app = Flask(__name__)

app.secret_key = '9a5c0aaf287745d3b21bb5a22e6dah0e9c8fb3bc39e34474f2f400f57'


@app.route('/')
def donate():
    return render_template('login.html')

@app.route('/charities')
def charities():
    return render_template('about.html')

@app.route('/login')
def rlogin():
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        session['username']=request.form['username']
        return render_template('about.html')
    elif request.method=='POST':
        user = {
        'username': request.form.get('username'),
        'password': request.form.get('password')
        }
        user = users.insert_one(user)
        session['username']=request.form['username']
        print(user)
        user_obj = users.find_one({'username': session['username']})
        return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('test.html')

@app.route('/donate')
def charity_index(): 
    donates=list(donations.find())
    for i in range(len(donates)):
      donates[i]['amount'] = float(donates[i]['amount'])
    donates.sort(key=lambda x: x['date'], reverse=False)
    user_obj = users.find_one({'username': session['username']})
    return render_template("charity_index.html", donations=donates, user_obj=user_obj, user=user_obj)

@app.route('/donations/new')
def donation_new():
    return render_template('donations_new.html')

@app.route('/donations', methods=['POST'])
def donation_submit():
    donation = {
        'name': request.form.get('charity-name'),
        'amount': request.form.get('amount'),
        'date': request.form.get('date'),
      }
    donations.insert_one(donation)
    return redirect(url_for('charity_index'))

@app.route('/donations/<donation_id>/remove', methods=['POST'])
def donation_del(donation_id):
    donations.delete_one({'_id': ObjectId(donation_id)})
    return redirect(url_for('charity_index'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)