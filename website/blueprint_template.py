from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from website.auth import login_required
from website.db import get_db

bp = Blueprint('blueprint_name', __name__, url_prefix='/...')


@bp.route('/')
def bp_index():
    return render_template('blueprint/index.html')