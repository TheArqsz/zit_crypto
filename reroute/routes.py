from flask import make_response, render_template, request, jsonify, abort, request, flash, session, Blueprint, redirect, url_for

rerouting_bp = Blueprint('rerouting_bp', __name__)

@rerouting_bp.route('/',methods=['GET'])
def main_page():
    return redirect(url_for("logged_out_bp.main_page"))