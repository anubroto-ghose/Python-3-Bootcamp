# Advanced SQL Operations with SQLAlchemy Core (2.x)
# This script demonstrates:
# - Table creation with foreign keys
# - Data insertion
# - Inner joins and foreign key joins
# - Subqueries and scalar subqueries
# - SELECT statements with joins and subqueries

from sqlalchemy import (
    MetaData, Table, Column, String, Integer,
    ForeignKey, select, create_engine, func
)

# Create a metadata object to hold table definitions
metadata = MetaData()

# Define 'user' table with id, username, fullname
user_table = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50)),
    Column("fullname", String(50)),
)

# Define 'address' table with foreign key to 'user'
address_table = Table(
    "address",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id"), nullable=False),
    Column("email_address", String(100), nullable=False),
)

# Create an in-memory SQLite database and create tables
engine = create_engine("sqlite:///some.db")
metadata.create_all(engine)

# Insert sample data into both tables within a transaction
with engine.begin() as conn:
    # Insert users
    conn.execute(
        user_table.insert(),
        [
            {"username": "ed", "fullname": "Ed Jones"},
            {"username": "jack", "fullname": "Jack Burger"},
            {"username": "wendy", "fullname": "Wendy Weathersmith"},
        ],
    )

    # Insert addresses linked to users by user_id
    conn.execute(
        address_table.insert(),
        [
            {"user_id": 1, "email_address": "ed@ed.com"},
            {"user_id": 1, "email_address": "ed@gmail.com"},
            {"user_id": 2, "email_address": "jack@yahoo.com"},
            {"user_id": 3, "email_address": "wendy@gmail.com"},
        ],
    )

# --- Join Examples ---

# Explicit inner join between user and address tables
join_obj = user_table.join(
    address_table, user_table.c.id == address_table.c.user_id
)
print(join_obj)

# Foreign key-based join (uses FK relationship)
print(user_table.join(address_table))

# SELECT all columns from both tables using join
stmt = (
    select(user_table, address_table)
    .select_from(user_table.join(address_table))
)

with engine.connect() as conn:
    print(conn.execute(stmt).fetchall())

# --- Subquery Example ---

# Subquery: count addresses per user
subq = (
    select(
        address_table.c.user_id,
        func.count(address_table.c.id).label("count"),
    )
    .group_by(address_table.c.user_id)
    .subquery()
)

# SELECT username and address count using join with subquery
stmt = (
    select(user_table.c.username, subq.c.count)
    .join(subq, user_table.c.id == subq.c.user_id)
    .order_by(user_table.c.username)
)

with engine.connect() as conn:
    print(conn.execute(stmt).fetchall())

# --- Scalar Subquery Example ---

# Scalar subquery: count addresses for each user
scalar_stmt = (
    select(func.count(address_table.c.id))
    .where(user_table.c.id == address_table.c.user_id)
    .scalar_subquery()
)

# SELECT username and address count using scalar subquery
stmt = select(user_table.c.username, scalar_stmt)

with engine.connect() as conn:
    print(conn.execute(stmt).fetchall())