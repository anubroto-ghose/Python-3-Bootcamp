"""
Basic SQLAlchemy ORM example (SQLAlchemy 2.x)

This file demonstrates:
- Declarative mapping
- Session lifecycle
- Insert, query, update, rollback
- Core ORM querying patterns
"""

from sqlalchemy import create_engine, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session,
)
from typing import Optional

# ---------------------------------------------------------
# Step 1: Declarative Base
# ---------------------------------------------------------
# DeclarativeBase is the modern replacement for declarative_base()
class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------
# Step 2: ORM-mapped class
# ---------------------------------------------------------
class User(Base):
    """
    ORM class mapped to the 'user' table.
    Each attribute maps to a column.
    """

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    fullname: Mapped[str] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"


# ---------------------------------------------------------
# Step 3: Create database engine
# ---------------------------------------------------------
# SQLite in-memory database (good for demos)
engine = create_engine("sqlite://", echo=False)

# Create tables from ORM metadata
Base.metadata.create_all(engine)


# ---------------------------------------------------------
# Step 4: Create a Session
# ---------------------------------------------------------
# Session manages:
# - transactions
# - identity map
# - flushing and committing
with Session(engine) as session:

    # -----------------------------------------------------
    # Step 5: Insert data
    # -----------------------------------------------------
    ed_user = User(name="ed", fullname="Edward Jones")
    session.add(ed_user)

    # Flush happens automatically before queries
    user_from_db = session.query(User).filter_by(name="ed").first()

    # Same Python object (identity map)
    assert ed_user is user_from_db

    # Insert multiple rows
    session.add_all(
        [
            User(name="wendy", fullname="Wendy Weathersmith"),
            User(name="mary", fullname="Mary Contrary"),
            User(name="fred", fullname="Fred Flinstone"),
        ]
    )

    # Modify an existing object (marks it as dirty)
    ed_user.fullname = "Ed Jones"

    # View pending and dirty objects
    session.new
    session.dirty

    # -----------------------------------------------------
    # Step 6: Commit
    # -----------------------------------------------------
    # Commit always flushes changes first
    session.commit()

    # -----------------------------------------------------
    # Step 7: Rollback example
    # -----------------------------------------------------
    ed_user.name = "Edwardo"
    fake_user = User(name="fake", fullname="Invalid User")
    session.add(fake_user)

    # Query triggers flush
    session.query(User).filter(User.name.in_(["Edwardo", "fake"])).all()

    # Rollback cancels transaction
    session.rollback()

    # Data is restored
    assert fake_user not in session
