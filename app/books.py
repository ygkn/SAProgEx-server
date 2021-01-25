from flask import Blueprint, request, jsonify

from app.db import get_db

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
        "id",
        "author",
        "title",
        "publisher",
        "price",
        "isbn",
    ):
        parameter_error.append(
            "invalid parameter: `sort-field` must be"
            "`ID` or `AUTHOR` or `TITLE` or `PUBLISHER` or `PRICE` or `ISBN`"
        )

    if len(parameter_error) != 0:
        return jsonify({"message": "\n".join(parameter_error)}), 400

    db = get_db()

    cur = db.cursor()

    books_with_next = []
    total = 0

    cur.execute(
        f"""
            select
                *
            from
                BOOKLIST
            where
                (
                    %(query)s is NULL or
                    (
                        TITLE like %(query)s
                        or AUTHOR like %(query)s
                        or PUBLISHER like %(query)s
                    )
                )
                and (
                    %(after)s is NULL or
                    {sort_field} {'>' if sort_direction == 'asc' else '<'} (
                    select
                        {sort_field}
                    from
                        BOOKLIST
                    where
                        ID=%(after)s
                    )
                )
            order by {sort_field} {sort_direction}
            limit %(count)s + 1
            """,
        {
            "query": f"%{query}%" if query != "" else None,
            "after": after,
            "count": count,
        },
    )

    books_with_next = list(cur)

    cur.execute(
        """
            select
                count(*)
            from
                BOOKLIST
            where
                (
                    %(query)s is NULL or
                    (
                        TITLE like %(query)s
                        or AUTHOR like %(query)s
                        or PUBLISHER like %(query)s
                    )
                )
        """,
        {"query": f"%{query}%" if query != "" else None},
    )
    total = cur.fetchone()["count"]

    items = books_with_next[:count]

    return jsonify(
        {"items": items, "total": total, "hasMore": len(books_with_next) > count}
    )


@bp.route("/suggestions")
def suggestions():
    """suggestions"""

    db = get_db()
    cur = db.cursor()

    query = request.args.get("query", default="")

    if query == "":
        return jsonify([])

    cur.execute(
        """
            select TITLE from BOOKLIST where TITLE like %(query)s
            union select AUTHOR from BOOKLIST where AUTHOR like %(query)s
            union select PUBLISHER from BOOKLIST where PUBLISHER like %(query)s
            order by 1 limit 10
        """,
        {"query": f"{query}%"},
    )
    books = cur
    print(list(cur))
    return jsonify([book["title"] for book in books])
