# SQL Expression Language (SQLAlchemy 2.x)
# This script demonstrates basic SQL operations using SQLAlchemy's Core API:
# - Table creation
# - SQL expressions (WHERE, AND, OR, IN, etc.)
# - Data insertion
# - SELECT, UPDATE, DELETE statements

from sqlalchemy import (
    MetaData, Table, Column, String, Integer,
    create_engine, select, and_, or_
)

# Define metadata object to hold table definitions
metadata = MetaData()

# Define 'user' table with columns: id, username, fullname
user_table = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50)),
    Column("fullname", String(50)),
)

# Create an in-memory SQLite database and create tables
engine = create_engine("sqlite:///some.db")
metadata.create_all(engine)

# --- SQL Expression Examples ---

# Simple equality comparison: username == 'ed'
print(user_table.c.username == "ed")

# Logical OR: username == 'ed' OR username == 'jack'
print((user_table.c.username == "ed") | (user_table.c.username == "jack"))

# Complex expression:
# fullname = 'ed jones' AND (username = 'ed' OR username = 'jack')
print(
    and_(
        user_table.c.fullname == "ed jones",
        or_(
            user_table.c.username == "ed",
            user_table.c.username == "jack",
        ),
    )
)

# Greater than comparison: id > 5
print(user_table.c.id > 5)

# IS NULL check: fullname IS NULL
print(user_table.c.fullname.is_(None))

# String concatenation: fullname + ' some name'
print(user_table.c.fullname + " some name")

# IN clause: username IN ('wendy', 'mary', 'ed')
print(user_table.c.username.in_(["wendy", "mary", "ed"]))

# --- Insert Data into Table ---

with engine.begin() as conn:
    conn.execute(
        user_table.insert(),
        [
            {"username": "ed", "fullname": "Ed Jones"},
            {"username": "jack", "fullname": "Jack Burger"},
            {"username": "wendy", "fullname": "Wendy Weathersmith"},
        ],
    )

# --- SELECT Queries ---

# Select username and fullname where username == 'ed'
stmt = select(user_table.c.username, user_table.c.fullname).where(
    user_table.c.username == "ed"
)

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)

# Select all rows from user table
with engine.connect() as conn:
    print(conn.execute(select(user_table)).fetchall())

# Select rows where username == 'ed' OR username == 'wendy'
stmt = select(user_table).where(
    or_(
        user_table.c.username == "ed",
        user_table.c.username == "wendy",
    )
)

with engine.connect() as conn:
    print(conn.execute(stmt).fetchall())

# --- UPDATE Statements ---

# Update fullname for user where username == 'jack'
with engine.begin() as conn:
    conn.execute(
        user_table.update()
        .where(user_table.c.username == "jack")
        .values(fullname="Jack Brown")
    )

# Update fullname for all users: set fullname = username + ' ' + fullname
with engine.begin() as conn:
    conn.execute(
        user_table.update().values(
            fullname=user_table.c.username + " " + user_table.c.fullname
        )
    )

# Print all rows after update
with engine.connect() as conn:
    print(conn.execute(select(user_table)).fetchall())

# --- DELETE Statement ---

# Delete user where username == 'jack'
with engine.begin() as conn:
    conn.execute(
        user_table.delete().where(user_table.c.username == "jack")
    )