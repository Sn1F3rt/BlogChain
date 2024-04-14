from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from .database import Base


class User(Base):
    __tablename__ = "users"

    address = Column(String(42), primary_key=True, nullable=False)
    username = Column(String(10), unique=True, nullable=True)
    nonce = Column(String(11), nullable=False)
    active = Column(Boolean, default=False, nullable=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.address

    def __repr__(self):
        return f"<User {self.address}>"


class Post(Base):
    __tablename__ = "posts"

    author = Column(String(10), primary_key=True, nullable=False)
    id = Column(String(8), primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(String(2000), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    def __repr__(self):
        return f"<Post {self.author} {self.id}>"


class Tip(Base):
    __tablename__ = "tips"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    sender = Column(String(10), nullable=False)
    recipient = Column(String(10), nullable=False)
    amount = Column(String(10), nullable=False)
    post_id = Column(String(8), nullable=False)
    tx_hash = Column(String(66), nullable=True)
    notified = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Tip {self.sender} {self.recipient}>"
