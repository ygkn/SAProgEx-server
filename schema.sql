DROP TABLE IF EXISTS BOOKLIST;

create table BOOKLIST(
    ID int primary key,
    AUTHOR varchar(256),
    TITLE varchar(512),
    PUBLISHER varchar(256),
    PRICE int,
    ISBN char(10)
)
