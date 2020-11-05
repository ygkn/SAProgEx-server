from flask import Blueprint, request, jsonify

from librarian.db import get_db

bp = Blueprint("book", __name__)


@bp.route("/")
def search():
    """search"""

    query = request.args.get("query", default="")
    after = request.args.get("after")
    count = request.args.get("count", default=50, type=int)
    sort_field = request.args.get("sort-field", default="ID")
    sort_direction = request.args.get("sort-direction", default="asc")

    parameter_error = []

    if not (1 <= count and count <= 50):
        parameter_error.append("invalid parameter: `count` must be between 1 and 50")

    if sort_direction not in ("asc", "desc"):
        parameter_error.append(
            "invalid parameter: `sort-direction` must be `asc` or `desc`"
        )

    if sort_field not in (
        "ID",
        "AUTHOR",
        "TITLE",
        "PUBLISHER",
        "PRICE",
        "ISBN",
    ):
        parameter_error.append(
            "invalid parameter: `sort-field` must be"
            "`ID` or `AUTHOR` or `TITLE` or `PUBLISHER` or `PRICE` or `ISBN`"
        )

    if len(parameter_error) != 0:
        return jsonify({"message": "\n".join(parameter_error)}), 400

    db = get_db()

    books_with_next = []
    total = 0

    books_with_next = db.execute(
        f"""
            select
                *
            from
                BOOKLIST
            where
                (
                    :query == "" or
                    (
                        TITLE like :query
                        or AUTHOR like :query
                        or PUBLISHER like :query
                    )
                )
                and (
                    :after is NULL or
                    {sort_field} {'>' if sort_direction == 'asc' else '<'} (
                    select
                        {sort_field}
                    from
                        BOOKLIST
                    where
                        ID=:after
                    )
                )
            order by {sort_field} {sort_direction}
            limit :count + 1
            """,
        {"query": f"%{query}%" if query != "" else "", "after": after, "count": count},
    ).fetchall()

    total = db.execute(
        """
            select
                count(*)
            from
                BOOKLIST
            where
                (
                    :query == "" or
                    (
                        TITLE like :query
                        or AUTHOR like :query
                        or PUBLISHER like :query
                    )
                )
        """,
        {"query": f"%{query}%" if query != "" else ""},
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
        {"items": items, "total": total, "hasMore": len(books_with_next) > count}
    )


@bp.route("/suggestions")
def suggestions():
    """suggestions"""

    db = get_db()
    query = request.args.get("query", default="")

    if query == "":
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
