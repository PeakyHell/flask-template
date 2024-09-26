import sqlite3
import click
from flask import current_app, g

def get_db():
    """
    Establishes a connection to the database if not connected to it yet.

    Returns:
        The connection to the database.
    """
    # If there is no connection to the database, connects to it
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    # Returns the database
    return g.db

def close_db(e=None):
    """
    If a connection to the database exists and it's not closed yet, closes it.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """
    Create the database tables using the schema.sql file.
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """
    Create the command 'init-db', usable in the terminal, to create the database tables.
    """
    init_db()
    click.echo('Initialized the database')

def init_app(app):
    """
    Tell the app to close the database when cleaning up and 
    add a new 'init-db' command that can be called using the flask command.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)