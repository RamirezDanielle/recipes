from flask import Flask, request, render_template, redirect, session, flash
from flask_app import app

from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def reg():
    print(request.form)
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'confirm_password' : request.form['confirm_password']
    }
    valid = User.validate_reg(data)
    if valid:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data['pw_hash'] = pw_hash
        user = User.save(data)
        session['user_id'] = user
        return redirect('/dashboard')
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid email or password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email or password', 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
