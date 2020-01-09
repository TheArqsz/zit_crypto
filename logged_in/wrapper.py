"""
wrapper.py
- creates wrappers for methods (for example @require_api_token)
"""

from flask import session, url_for, request, redirect
from functools import wraps
from database.models import User
import logging
def require_api_token(func):
    """ 
    Requires api token from cookie
    
    Parameters
    ----------
    func: 
        action requested on method

    Returns
    -------
    If succeded:        passes further requests
    If not succeded:    aborts with 403 status code (Unauthorized)
    """
    @wraps(func)
    def check_token(*args, **kwargs):
        if 'ACCESS_TOKEN' not in session:
            # Deny if not authorized
            return redirect(url_for('logged_out_bp.main_page'))
        else:
            api_token = session['ACCESS_TOKEN']
            # Check if authorized - 1 if yes; Rest is no
            valid_login = User.decode_token(api_token)
            if not isinstance(valid_login,int):
                session.pop('ACCESS_TOKEN', None)
                session.pop('username', None)
                return redirect(url_for('logged_out_bp.main_page'))
        # Pass whatever arrived if authorized
        return func(*args, **kwargs)

    return check_token