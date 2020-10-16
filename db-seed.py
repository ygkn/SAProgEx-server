import csv
import sqlite3

db_path = "bookdb.db"

con = sqlite3.connect(db_path)
cur = con.cursor()

try:
    cur.execute(
        """
        create table BOOKLIST(
            ID int primary key,
            AUTHOR varchar(256),
            TITLE varchar(512),
            PUBLISHER varchar(256),
            PRICE int,
            ISBN char(10)
        )
        """
    )

    with open("./BookList.csv", "r") as file:
        reader = csv.reader(file)
        for line in reader:
            cur.execute("insert into BOOKLIST values (?,?,?,?,?,?);", line)

except sqlite3.Error as e:
    print("Error occurred:", e.args[0])

con.commit()
con.close()
