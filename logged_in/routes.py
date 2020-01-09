from flask import redirect, make_response, jsonify, abort, request, flash, session, url_for, Blueprint, redirect, render_template
from werkzeug.utils import secure_filename
from database.models import db, User
from datetime import datetime
from logged_in.hash_cracker import hash_types, hasher
from time import perf_counter, strftime, gmtime
from os import remove, path
from mimetypes import guess_extension
from logged_in.archive_cracker import file_handler
from multiprocessing import TimeoutError
from multiprocessing.pool import ThreadPool
import logging
from sqlalchemy.exc import IntegrityError
from .wrapper import require_api_token
from logged_in.hash_encoder import encoder
import threading
from mail.mail_helper import send_arch_message
import copy
from base64 import b64encode
from werkzeug.exceptions import RequestEntityTooLarge
from humanfriendly import format_timespan

logged_in_bp = Blueprint('logged_in_bp', __name__, template_folder='templates', static_folder='static')


@logged_in_bp.route('/index', methods=['GET'])
@require_api_token
def index():
    return "Hello, World!"

@logged_in_bp.route('/', methods=["GET"])
@logged_in_bp.route('/home', methods=["GET"])
@require_api_token
def home_page():
    return render_template("solve.htm", username=session['username'])

@logged_in_bp.route('/logout', methods=['POST'])
@require_api_token
def log_out():
    logging.info('[LOGOUT] Got logout request')
    session.pop('ACCESS_TOKEN', None)
    session.pop('username', None)
    return redirect(url_for('logged_out_bp.main_page'))

@logged_in_bp.route('/settings', methods=['POST', 'GET'])
@require_api_token
def settings():
    logging.info('[SETTINGS] Got settings request')
    if request.method == 'GET':
        return render_template("solve.htm", settings=1)
    else:
        form = request.form
        print(form.get('test'))
        flash('Clicked', category='message')
        return render_template("solve.htm", settings=1)

@logged_in_bp.route('/deleteUser', methods=['DELETE', 'GET'])
@require_api_token
def delete_user():
    logging.info('[DELETE] Got delete user request')
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        abort(400, "USER DOES NOT EXIST") #TODO
    else:
        db.session.delete(user)
        db.session.commit()
        session.pop('ACCESS_TOKEN', None)
        session.pop('username', None)
        flash('User deleted', category='message')
        return redirect(url_for('logged_out_bp.main_page'))

@logged_in_bp.route('/arch', methods=['GET'])
@require_api_token
def arch():
    return render_template('solve.htm', arch=1)
    
@logged_in_bp.route('/hash/encode', methods=['POST', 'GET'])
@require_api_token
def hash_encoder():
    if request.method == 'GET':
        return render_template('solve.htm', hash_encode=1)
    else:
        logging.info('[HASH] Got hash encode request')
        text_to_hash = request.form.get('text_to_encode')
        mode = request.form.get('mode')
        if text_to_hash == "":
            flash('No text provied', 'error')
            return render_template('solve.htm', hash_encode=1)
        start_time = perf_counter()
        hashed = encoder.encode(text=text_to_hash, mode=mode)
        elapsed_time = perf_counter() - start_time  
        data = {
            "Original": text_to_hash,
            "Encoded": hashed,
            "Mode": mode,
            "Encoding duration": format_timespan(elapsed_time),
        }
        return render_template('solve.htm', hash_encode=1, data=data)

@logged_in_bp.route('/hash/decode', methods=['POST', 'GET'])
@require_api_token
def hash_decoder():
    if request.method == 'GET':
        return render_template('solve.htm', hash_decode=1)
    else:
        logging.info('[HASH] Got hash decode request')
        hash_to_crack = request.form.get('hash_encoded')
        if hash_to_crack is None:
            return render_template("solve.htm", hash_decode=1, error=NO_HASH_MESSAGE)
        else:
            hash_type = hash_types.get_hash_type(hash_to_crack)
            if hash_type:
                start_date = datetime.now()
                start_time = perf_counter()
                dehashed = hasher.single(hash_to_crack, hash_type)
                elapsed_time = perf_counter() - start_time
                end_date = datetime.now()
                if dehashed:
                    data = {
                        'Selected hash type': hash_types.get_hash_type(hash_to_crack),
                        'Original hash': hash_to_crack,
                        'Decoded hash': dehashed,
                        'Dehashing duration': format_timespan(elapsed_time),
                        'Dehash started at': str(start_date.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]),
                        'Dehash ended at': str(end_date.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
                    }
                    return render_template('solve.htm', hash_decode=1, data=data)
                else:
                    flash(CANNOT_DECRYPT_MESSAGE)
                    return render_template('solve.htm', hash_decode=1) 
            else:
                flash(NOT_CORRECT_HASH_MESSAGE)
                return render_template('solve.htm', hash_decode=1) 


@logged_in_bp.route('/arch/decode', methods=['POST', 'GET'])
@require_api_token
def archive_decode():
    if request.method == 'GET':
        return render_template("solve.htm", arch=1 )
    else:
        logging.info('[ARCH] Got archive decrypt request')
        try:
            if not 'file' in request.files:
                return render_template("solve.htm", arch=1, error=NO_FILE_ERROR_MESSAGE) 
            else:
                arch_file = request.files.get('file')
                arch_temp_file = request.files.get('file')
                arch_file_name = secure_filename(arch_file.filename)
                arch_file_path = path.join(TEMP_PATH, str(int(datetime.now().timestamp())))
                arch_file.save(arch_file_path)
                arch_file_mime_type = file_handler.get_file_mime_type(arch_file_path)
                if arch_file_mime_type not in file_handler.get_allowed_mime_types():
                    flash(f'Wrong file type provided: {guess_extension(arch_file_mime_type, strict=False)}', 'error')
                    return render_template("solve.htm", arch=1)
                else:
                    
                    user = User.query.filter_by(username=session['username']).first()
                    thread = threading.Thread(target=decrack, args=(arch_file_path, arch_file_mime_type, arch_file_name, user.username, user.email))
                    thread.daemon = True                    
                    thread.start()
                    message = f"""
                    Archive will be tried to hack in next: {format_timespan(DECRACK_TIMEOUT)}.
                    Answer will be sent to your email.
                    """
                    flash(message, 'message')
                    return render_template("solve.htm", arch=1 )
        except RequestEntityTooLarge as e:
            message = 'File too large'
            flash(message, 'error')
            logging.info("[ARCH] " + e.description)
            return render_template("solve.htm", arch=1)
           

def decrack(arch_file_path, arch_file_mime_type, arch_file_name, username, email):
    
    start_date = datetime.now()
    start_time = perf_counter()
    pool = ThreadPool(processes=1)
    pool_result = pool.apply_async(file_handler.handle_file, (arch_file_path, arch_file_mime_type))
    try:
        password = pool_result.get(timeout=DECRACK_TIMEOUT)
    except TimeoutError as e:
        pool.terminate()
        logging.info(f'[ARCH] Archive cannot be decrypted after given time of {format_timespan(DECRACK_TIMEOUT)}')
        send_arch_message(user=username, mail=email, file_name=arch_file_name,time=DECRACK_TIMEOUT)
        return
    elapsed_time = perf_counter() - start_time
    end_date = datetime.now()
    pool.terminate()   
    duration_message = f"""
    <div>Cracking password started at: {start_date}</div>
    <div>Cracking password ended at: {end_date}</div>
    """
    file_handler.clear_file(arch_file_path)
    send_arch_message(user=username, mail=email, password=password, file_name=arch_file_name, time=elapsed_time, additional_info=duration_message)

@logged_in_bp.errorhandler(404)
def not_found(error):
    logging.info(f'[ERROR] {error}')
    return make_response(jsonify(
        {
            'error': 'Not found',
            'timestamp': datetime.now()
        }
    ), 404)


@logged_in_bp.errorhandler(500)
def not_found(error):
    logging.info(f'[ERROR] {error}')
    return make_response(jsonify(
        {
            'error': 'Server error',
            'timestamp': datetime.now()
        }
    ), 500)


@logged_in_bp.errorhandler(413)
def request_entity_too_large(error):
    message = 'File too large'
    flash(message, 'error')
    logging.info("[ARCH] File too large")
    return render_template("solve.htm", arch=1)


@logged_in_bp.errorhandler(400)
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



class TimeoutException(Exception): pass

def try_time_limit(duration_sec):
    import signal
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(duration_sec) 
 
def signal_handler(signum, frame):
    raise TimeoutException()


from tempfile import gettempdir
TEMP_PATH = gettempdir()

BAD_TYPE_ERROR_MESSAGE = 'Bad type'
NO_FILE_ERROR_MESSAGE = 'No file was provided'
NOT_CORRECT_HASH_MESSAGE = 'This hash is not correct'
CANNOT_DECRYPT_MESSAGE = "Hash cannot be decrypted"
CANNOT_DECRYPT_FILE_MESSAGE = "File cannot be decrypted"
NO_HASH_MESSAGE = 'No hash provided'
BAD_REQUEST_MESSAGE = 'Incorrect request data'

import os
DECRACK_TIMEOUT = os.getenv('ARCHIVE_DECRACK_TIMEOUT', 1200)