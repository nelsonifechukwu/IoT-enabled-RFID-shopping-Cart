from app import app 
from flask import session, make_response, redirect, render_template, request, flash, url_for, Response, jsonify
from app.models import checklogin, delete_product_data, get_products_data, update_uid, get_all_uids, add_tags, tag_exist 
import json, random

API = 'xdol'

#login
@app.route('/', methods = ('GET', 'POST'))
@app.route('/login' , methods = ["GET", "POST"])
def login():
    if (request.method=='POST'):
        username = request.form['username']
        password = request.form['password']
        users = checklogin()
        if username == users[0][0] and password == users[0][1]:
            session['user'] = username
            flash('User Login Successfull')
            return redirect(url_for('shop'))
        elif username == users[1][0] and password == users[1][1]:
            session['admin'] = username
            flash('Admin Login Successfull')
            return redirect(url_for('add'))
        else:
            flash('Error: Invalid Username or Password')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

#plot data
@app.route('/shop')
def shop():
    #create a session to secure this endpoint
    if "user" not in session:
        return redirect(url_for('login'))
    data = get_products_data() 
    return render_template('shop.html', name=session["user"], data = data)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if "admin" not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        tag_id = request.form['tag_id']
        name = request.form['name']

        succeed = tag_exist(tag_id)
        
        if succeed == False:
            flash('Error: TAG Already Added. Please Register a New Tag')
            return redirect(url_for('add'))
        
        elif succeed == True:
            flash('Added {name}-{tag_id} to Shop'.format(name= name, tag_id= tag_id))
            add_tags(tag_id, name)
            return redirect(url_for('shop'))
    else:
        return render_template('create.html')

#update button state
@app.route('/update_uid/tag=<id>', methods = ['GET', 'POST'])
def update_state(id):
    if (update_uid(id)):
        return str(1)
    else:
        return str(0)

#delete all data
@app.route('/delete/tag=<tag_id>', methods = ['GET', 'POST'])
def delete(tag_id):
        delete_product_data(tag_id)
        return redirect(url_for('shop'))

#logout of session
@app.route('/logout', methods=['POST'])
def log_out():
    if "user" in session:
        session.pop("user")
    else:
        session.pop("admin")
    return redirect(url_for('login'))

@app.route('/get_uids/<tag_id>', methods=['GET'])
def get_uids(tag_id):
    uids = get_all_uids()
    for uid in uids:
        if tag_id == uid[0]:
            return str(1)
        
    return str(0)

