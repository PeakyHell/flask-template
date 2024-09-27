from flask_sqlalchemy import SQLAlchemy
import click

db = SQLAlchemy()

def init_app(app):

    db.init_app(app)

    @app.cli.command('init-db')
    def init_db_command():
        db.create_all()
        click.echo('Initialized the database.')