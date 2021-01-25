import os

from flask import Flask


def create_app(test_config=None) -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.environ.get("DATABASE_URL"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.after_request
    def add_header(res):
        res.headers["Access-Control-Allow-Origin"] = "*"
        return res

    @app.route("/")
    def hello():
        return "Hi! How is it going?"

    from app import db

    db.init_app(app)

    # apply the blueprints to the app
    from app import books

    app.register_blueprint(books.bp, url_prefix="/books")

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
