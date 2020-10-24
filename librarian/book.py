from flask import Blueprint, request, jsonify

from librarian.db import get_db

bp = Blueprint("book", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""

    db = get_db()
    query = request.args.get("query")

    if query is None:
        books = db.execute("select * from BOOKLIST").fetchall()

        return jsonify(
            [
                dict(
                    ID=book["ID"],
                    AUTHOR=book["AUTHOR"],
                    TITLE=book["TITLE"],
                    PUBLISHER=book["PUBLISHER"],
                    PRICE=book["PRICE"],
                    ISBN=book["ISBN"],
                )
                for book in books
            ]
        )

    books = db.execute(
        """
            select
                *
            from
                BOOKLIST
            where
                TITLE like ?
                or AUTHOR like ?
                or PUBLISHER like ?""",
        (f"%{query}%",) * 3,
    ).fetchall()
    return jsonify(
        [
            dict(
                ID=book["ID"],
                AUTHOR=book["AUTHOR"],
                TITLE=book["TITLE"],
                PUBLISHER=book["PUBLISHER"],
                PRICE=book["PRICE"],
                ISBN=book["ISBN"],
            )
            for book in books
        ]
    )
