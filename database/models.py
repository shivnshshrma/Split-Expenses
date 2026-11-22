import uuid
from sqlalchemy import Boolean, Column, Numeric, String, Integer, ForeignKey, JSON, DateTime, UniqueConstraint, func, true
from database.connection import Base



class User(Base):
    __tablename__ = "users"

    username = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    is_active = Column(Boolean, server_default=true(), nullable=False)


class Group(Base):
    __tablename__ = "groups"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_by = Column(String, ForeignKey("users.username"), nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class GroupMember(Base):
    __tablename__ = "group_members"
    __table_args__ = (UniqueConstraint(
        # Ensure that user can be added only once to a group
        # This is a unique constraint on the combination of group_id and user_id
        "group_id", "user_id", name="unique_group_user"
    ), )

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(String, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("users.username", ondelete="CASCADE"), nullable=False)
    role = Column(String, server_default="member", nullable=False)
    joined_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Expense(Base):
    __tablename__ = "expenses"
   

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    group_id = Column(String, ForeignKey("groups.id", ondelete="CASCADE"), nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(String, nullable=True)
    split_type = Column(String, nullable=False, server_default="equal")
    split_with = Column(JSON, nullable=True)
    is_active = Column(Boolean, server_default=true(), nullable=False) 
