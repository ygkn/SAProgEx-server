from flask import Blueprint, request, jsonify

from librarian.db import get_db

bp = Blueprint("book", __name__)


@bp.route("/search")
def search():
    """search"""

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


@bp.route("/suggestions")
def suggestions():
    """suggestions"""

    db = get_db()
    query = request.args.get("query")

    if query is None:

        return jsonify([])

    books = db.execute(
        """
            select TITLE from BOOKLIST where TITLE like ?
            union select AUTHOR from BOOKLIST where AUTHOR like ?
            union select PUBLISHER from BOOKLIST where PUBLISHER like ?
            order by 1 limit 10
        """,
        (f"{query}%",) * 3,
    ).fetchall()
    return jsonify([book["TITLE"] for book in books])
