#! /usr/bin/env python3

import sqlite3
from cgi import FieldStorage
from html import escape


def form() -> str:
    form_data = FieldStorage()
    query: str = form_data.getvalue("query", "")

    return f"""
        <form action="" method="GET" class="flex w-full">
            <input
            type="search"
            name="query"
            placeholder="検索キーワードを入力……"
            class="p-3 shadow rounded-full focus:outline-none focus:shadow-outline flex-grow"
            value={query}
            required
            />
            <label for="query" class="sr-only">検索キーワードを入力</label>
            <button
            type="submit"
            class="ml-4 bg-blue-500 text-white px-4 rounded focus:outline-none focus:shadow-outline"
            >
            検索
            </button>
        </form>
    """

def book_table_row(a) -> str:
    return f"""
        <tr class="{"bg-gray-100" if a[0] % 2 is 0 else ""}">
            <td class="p-3">{a[1]["ID"]}</td>
            <td class="p-3">{a[1]["AUTHOR"]}</td>
            <td class="p-3">{a[1]["TITLE"]}</td>
            <td class="p-3">{a[1]["PUBLISHER"]}</td>
            <td class="p-3">{a[1]["PRICE"]}</td>
            <td class="p-3">{a[1]["ISBN"]}</td>
        </tr>
    """



def book_table() -> str:
    form_data = FieldStorage()
    query: str = form_data.getvalue("query", "")

    if query == "":
        return ""

    db_path = "bookdb.db"

    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    try:
        cur.execute("""
            select
                *
            from
                BOOKLIST
            where
                TITLE like ?
                or AUTHOR like ?
                or PUBLISHER like ?""", (f"%{query}%",) * 3 )

        rows= cur.fetchall()


        return f"""
            <p class="my-6">"<b>{escape(query)}</b>" の検索結果 {len(rows)} 件</p>

            <table>
              <thead>
                <th class="sticky top-0 bg-white">ID</th>
                <th class="sticky top-0 bg-white">著者</th>
                <th class="sticky top-0 bg-white">タイトル</th>
                <th class="sticky top-0 bg-white">出版社</th>
                <th class="sticky top-0 bg-white">値段</th>
                <th class="sticky top-0 bg-white">ISBN</th>
              </thead>
              <tbody>
                  {''.join(map(book_table_row, enumerate(rows)))}
              </tbody>
            </table>

            """


    except sqlite3.Error as e:
        return "Error occurred:" + e.args[0]



# HTTP Header
print("Content-type: text/html\n")


# Body
print(
    f"""
<!DOCTYPE html>
<html lang="ja" class="min-h-full">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>検索 - 書籍管理システム</title>
    <link
      href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css"
      rel="stylesheet"
    />
  </head>
  <body class="min-h-full p-4">
    <div class="min-h-full max-w-screen-md mx-auto">
      <h1 class="text-4xl mb-8"><a href="?">書籍検索くん</a></h1>
      {form()}
    </div>

    {book_table()}
  </body>
</html>


"""
)
