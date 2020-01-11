from flask import make_response, render_template, request, jsonify, abort, request, flash, session, Blueprint, redirect, url_for
from werkzeug.utils import secure_filename
from database.models import db, User
from datetime import datetime
from time import perf_counter
from os import remove, path
import logging
from sqlalchemy.exc import IntegrityError

logged_out_bp = Blueprint('logged_out_bp', __name__, template_folder='templates', static_folder='static')

@logged_out_bp.route('/',methods=['GET'])
@logged_out_bp.route('/main',methods=['GET'])
def main_page():
    return render_template("login.html")

@logged_out_bp.route('/signin', methods=['POST'])
def sign_in_user():
    logging.info('[SIGNIN] Got sign in request')
    form = request.form
    user = User.query.filter_by(username=form['uname']).first()
    if user and user.check_password(form['pwd']):
        access_token = user.generate_token(user.id)
        if access_token:
            session['ACCESS_TOKEN'] = access_token.decode()
            session['username'] = user.username
            logging.info(f'[LOGIN] User {user.username} successfuly logged in')
            return redirect(url_for('logged_in_bp.home_page'))
        else:
            # User does not exist. Therefore, we return an error message
            flash("Wrong username or password", 'error')
            return redirect(url_for('logged_out_bp.main_page'))
    else:
        flash("Wrong username or password", 'error')
        return redirect(url_for('logged_out_bp.main_page'))

@logged_out_bp.route('/signUp', methods=['POST'])
def sign_up_user():
    logging.info('[SIGNUP] Got sign up request')
    username = request.form.get('uname')
    pwd = request.form.get('pwd')
    email = request.form.get('email')
    if username is None or pwd is None or email is None:
        flash('Wrong data provided', category='error')
        return redirect(url_for('logged_out_bp.main_page')) 
    else:
        user = User(username=username, email=email)
        user.set_password(pwd)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError as e:
            print(e)
            flash('User exists', category='error')
            return redirect(url_for('logged_out_bp.main_page'))
        flash('User created', category='message')
        return redirect(url_for('logged_out_bp.main_page'))

@logged_out_bp.errorhandler(404)
def not_found(error):
    logging.info(f'[ERROR] {error}')
    return make_response(jsonify(
        {
            'error': 'Not found',
            'timestamp': datetime.now()
        }
    ), 404)


@logged_out_bp.errorhandler(500)
def not_found(error):
    logging.info(f'[ERROR] {error}')
    return make_response(jsonify(
        {
            'error': 'Server error',
            'timestamp': datetime.now()
        }
    ), 500)


@logged_out_bp.errorhandler(400)
def not_handled(error):
    logging.info(f'[ERROR] {error}')
    if error:
        return make_response(jsonify(
            {
                'error': error.description,
                'timestamp': datetime.now()
            }
        ), 400)
    else:
        return make_response(jsonify(
            {
                'error': 'Cannot proceed this request',
                'timestamp': datetime.now()
            }
        ), 400)
