import psycopg2
from psycopg2.extras import RealDictCursor

import csv

import click
from flask import current_app, g, Flask
from flask.cli import with_appcontext


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = psycopg2.connect(
            current_app.config["DATABASE"],
        )

    g.db.cursor_factory = RealDictCursor

    return g.db


def close_db(e=None) -> None:
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    try:
        db = get_db()
        cur = db.cursor()

        with current_app.open_resource("../schema.sql") as f:
            cur.execute(f.read().decode("utf8"))

        with current_app.open_resource("../BookList.csv", "r") as file:
            reader = csv.reader(file)
            for line in reader:
                print(list(line))
                cur.execute(
                    "insert into BOOKLIST values (%s,%s,%s,%s,%s,%s);",
                    [c if c != "" else None for c in line],
                )

        db.commit()

    except psycopg2.Error as e:
        print("Error occurred:", e.args[0])


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app: Flask):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
