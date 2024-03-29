#!/usr/bin/python3
# views.py

from flask import Flask, render_template, request, redirect, url_for, flash
from auth.forms import RegistrationForm
# Routes for registration, login, and logout
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process registration form submission
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Login form handling
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Logout logic
    return render_template('logout.html')



