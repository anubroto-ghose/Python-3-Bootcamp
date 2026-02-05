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
#:param echo=False: if True, the Engine will log all statements
# as well as a ``repr()`` of their parameter lists to the default log
# handler, which defaults to ``sys.stdout`` for output.   If set to the
# string ``"debug"``, result rows will be printed to the standard output
engine = create_engine("sqlite:///some.db", echo=False)

# Create tables from ORM metadata
Base.metadata.create_all(engine)


# ---------------------------------------------------------
# Step 4: Create a Session
# ---------------------------------------------------------
# Session manages:
# - transactions
# - identity map
# - flushing and committing
# Open a Session (Unit of Work)
# -----------------------------------------------------
# Session represents:
# - a database transaction
# - an identity map (one Python object per DB row)
# - a change tracker (new / dirty / deleted objects)
#
# Nothing is written to the database unless the Session
# flushes or commits.
with Session(engine) as session:

    # -------------------------------------------------
    # Step 1: Create a new ORM object (NOT in DB yet)
    # -------------------------------------------------
    # This creates a plain Python object.
    # At this point:
    # - No SQL has been executed
    # - The object is NOT stored in the database
    ed_user = User(name="ed", fullname="Edward Jones")

    # Add the object to the Session
    # The object state becomes: PENDING
    session.add(ed_user)

    # -------------------------------------------------
    # Step 2: Run a query (auto-flush happens here)
    # -------------------------------------------------
    # Before executing a SELECT, SQLAlchemy automatically
    # FLUSHES pending changes to keep DB + memory in sync.
    #
    # FLUSH means:
    # - INSERT is sent to DB
    # - Transaction is still OPEN
    # - Data is NOT permanently saved yet
    user_from_db = session.query(User).filter_by(name="ed").first()

    # -------------------------------------------------
    # Step 3: Identity Map guarantee
    # -------------------------------------------------
    # SQLAlchemy guarantees:
    # "One database row = one Python object per Session"
    #
    # So the object we inserted and the object we queried
    # are actually the SAME Python object in memory.
    assert ed_user is user_from_db

    # -------------------------------------------------
    # Step 4: Add multiple new objects at once
    # -------------------------------------------------
    # All these objects are placed in PENDING state.
    # Still no SQL is executed yet.
    session.add_all(
        [
            User(name="wendy", fullname="Wendy Weathersmith"),
            User(name="mary", fullname="Mary Contrary"),
            User(name="fred", fullname="Fred Flinstone"),
        ]
    )

    # -------------------------------------------------
    # Step 5: Modify an existing object
    # -------------------------------------------------
    # Changing an attribute marks the object as DIRTY.
    # SQLAlchemy tracks this automatically.
    # No UPDATE SQL yet.
    ed_user.fullname = "Ed Jones"

    # -------------------------------------------------
    # Step 6: Inspect Session state
    # -------------------------------------------------
    # session.new:
    # - Objects added but not flushed yet
    # - Will generate INSERT statements on flush
    session.new

    # session.dirty:
    # - Objects modified since last flush
    # - Will generate UPDATE statements on flush
    session.dirty

    # -------------------------------------------------
    # NOTE:
    # SQL is sent to DB only when:
    # - a query triggers an auto-flush
    # - session.flush() is called explicitly
    # - session.commit() is called
    #
    # session.commit() would:
    # 1. Flush all pending + dirty objects
    # 2. COMMIT the transaction
    # 3. Make changes permanent


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
