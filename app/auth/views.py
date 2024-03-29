#!/usr/bin/python3
""" Authentication views """
from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token()
        send_email(user.email, Please confirm your account,
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to your account')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """ Confirm sent token """
    if current_user.is_confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Your account has been cofirmed. Welcome!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    """ Resend confirmation email """
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you via email.')
    return redirect(url_for('main.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.first())
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.keep_logged_in.data)
            next = request.args.get('next')
            if next is None or not next startswith('/'):
                next = url_for('main.index')
                return redirect(next)
        flash('Invalid email or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out of your account.')
    return redirect(url_for('main.index'))
