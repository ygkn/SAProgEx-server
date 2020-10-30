from flask import Blueprint, request, jsonify

from librarian.db import get_db

bp = Blueprint("book", __name__)


@bp.route("/")
def search():
    """search"""

    query = request.args.get("query")
    after = request.args.get("after", default=0, type=int)
    count = request.args.get("count", default=50, type=int)

    db = get_db()

    books_with_next = []
    total = 0

    if query is None:
        books_with_next = db.execute(
            """
                select
                    *
                from
                    BOOKLIST
                where
                    ID > ?
                order by ID asc
                limit ? + 1
            """,
            (after, count),
        ).fetchall()

        total = db.execute("select count(*) from BOOKLIST").fetchone()["count(*)"]
    else:
        like_params = (f"%{query}%",) * 3

        books_with_next = db.execute(
            """
                select
                    *
                from
                    BOOKLIST
                where
                    (
                        TITLE like ?
                        or AUTHOR like ?
                        or PUBLISHER like ?
                    )
                    and ID > ?
                order by ID asc
                limit ? + 1
                """,
            like_params
            + (
                after,
                count,
            ),
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
            like_params,
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
        for book in books_with_next[0:count]
    ]

    return jsonify(
        {"items": items, "total": total, "hasMany": len(books_with_next) > count}
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
