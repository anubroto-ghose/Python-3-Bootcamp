"""
Advanced SQLAlchemy ORM (SQLAlchemy 2.x)

This file demonstrates:
- Relationships
- Cascades
- Joins (implicit & explicit)
- Aliasing
- Subqueries
- Eager loading strategies
"""

from sqlalchemy import (
    create_engine,
    String,
    Integer,
    ForeignKey,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
    aliased,
    joinedload,
    subqueryload,
    contains_eager,
)

# ---------------------------------------------------------
# Base
# ---------------------------------------------------------
class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------
# User entity
# ---------------------------------------------------------
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    fullname: Mapped[str] = mapped_column(String(100))

    # One-to-many relationship
    addresses: Mapped[list["Address"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"User(name={self.name})"


# ---------------------------------------------------------
# Address entity
# ---------------------------------------------------------
class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(100), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # Many-to-one relationship
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self):
        return f"Address(email={self.email_address})"


# ---------------------------------------------------------
# Database setup
# ---------------------------------------------------------
engine = create_engine("sqlite://", echo=False)
Base.metadata.create_all(engine)


# ---------------------------------------------------------
# Insert data
# ---------------------------------------------------------
with Session(engine) as session:

    jack = User(
        name="jack",
        fullname="Jack Bean",
        addresses=[
            Address(email_address="jack@gmail.com"),
            Address(email_address="j25@yahoo.com"),
            Address(email_address="jack@hotmail.com"),
        ],
    )

    session.add(jack)
    session.commit()


# ---------------------------------------------------------
# Querying & Joins
# ---------------------------------------------------------
with Session(engine) as session:

    # Implicit join (via WHERE)
    session.query(User, Address).filter(User.id == Address.user_id).all()

    # Explicit join
    session.query(User, Address).join(Address).all()

    # Best practice: join via relationship
    session.query(User, Address).join(User.addresses).all()

    # Filtering via joined table
    session.query(User.name).join(User.addresses).filter(
        Address.email_address == "jack@gmail.com"
    ).first()

    # -----------------------------------------------------
    # Aliasing (same table joined multiple times)
    # -----------------------------------------------------
    a1 = aliased(Address)
    a2 = aliased(Address)

    session.query(User).join(a1).join(a2).filter(
        a1.email_address == "jack@gmail.com",
        a2.email_address == "jack@hotmail.com",
    ).all()

    # -----------------------------------------------------
    # Subquery + aggregation
    # -----------------------------------------------------
    subq = (
        session.query(
            User.id.label("user_id"),
            func.count(Address.id).label("address_count"),
        )
        .join(User.addresses)
        .group_by(User.id)
        .subquery()
    )

    session.query(
        User.name,
        func.coalesce(subq.c.address_count, 0),
    ).outerjoin(subq, User.id == subq.c.user_id).all()

    # -----------------------------------------------------
    # Eager loading examples
    # -----------------------------------------------------

    # N+1 problem (lazy loading)
    for user in session.query(User):
        user.addresses

    # subqueryload (two queries)
    for user in session.query(User).options(subqueryload(User.addresses)):
        user.addresses

    # joinedload (single LEFT OUTER JOIN)
    for user in session.query(User).options(joinedload(User.addresses)):
        user.addresses

    # contains_eager (manual join + eager)
    for addr in (
        session.query(Address)
        .join(Address.user)
        .options(contains_eager(Address.user))
    ):
        addr.user
