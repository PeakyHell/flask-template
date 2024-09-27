import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash

from website.db import db
from website.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Create the register view
@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    Register page view.
    If the register form is sent, create and insert a new user into the database then send the user to the login page.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        # Ensure that both input were filled
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                # Create and insert a new user into the database
                new_user = User(
                    username=username,
                    password = generate_password_hash(password)
                )
                db.session.add(new_user)
                db.session.commit()

            except Exception as e:
                error = f"User {username} is already registered."
            else:
                # Sends the user to the login page
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Login page view.
    If the login form is sent, looks for the user in the database and connects it then sends it to the index page.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        # Search for the user in the database
        user = User.query.filter_by(username=username).first()

        # Verify that the user exists and that the password is correct
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        # Saves the user session in a cookie then redirects the user to the index page
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """
    If a cookie containing the user session, automatically connects the user.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout')
def logout():
    """
    Disconnects the user.
    """
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """
    Decorator that require the use to be logged in to acces a page.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view