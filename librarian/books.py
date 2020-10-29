from flask import Blueprint, request, jsonify

from librarian.db import get_db

bp = Blueprint("book", __name__)


@bp.route("/")
def search():
    """search"""

    db = get_db()
    query = request.args.get("query")

    books = []
    total = 0

    if query is None:
        books = db.execute("select * from BOOKLIST").fetchall()
        total = db.execute("select count(*) from BOOKLIST").fetchone()["count(*)"]
    else:
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
        total = db.execute(
            """
                select
                    count(*)
                from
                    BOOKLIST
                where
                    TITLE like ?
                    or AUTHOR like ?
                    or PUBLISHER like ?""",
        ).fetchone()["count(*)"]

    items = [
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

    return jsonify({"items": items, "total": total})


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
