import os

from flask import Flask

def create_app(test_config=None):
    """
    Create a Flask app with a database and some basic routes.

    Args:
        test_config (idk): Configuration used for tests.

    Returns:
        the created Flask app.
    """

    # Create a Flask app, its config files are in the instance folder
    app = Flask(__name__, instance_relative_config=True)
    # Configure the app, it has a database that will be placed inside the instance folder
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'website.sqlite')
    )

    # If no test config is given, the app will use its config, else it will use the test config
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Create a simple page that says Hello, World!
    @app.route('/hello')
    def hello():
        return "Hello, World!"

    from . import db
    db.init_app(app)

    # Import the Blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    return app