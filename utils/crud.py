from .models import User, Post, Tip
from .database import create_session


def get_user_by_address(address: str):
    session = create_session()
    user = session.query(User).filter(User.address == address).first()
    session.close()

    return user


def get_user_by_username(username: str):
    session = create_session()
    user = session.query(User).filter(User.username == username).first()
    session.close()

    return user


def add_user(address: str, nonce: str):
    session = create_session()
    user = User(address=address, nonce=nonce)
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()

    return user


def activate_user(address: str):
    session = create_session()
    user = session.query(User).filter(User.address == address).first()
    user.active = True
    session.commit()
    session.refresh(user)
    session.close()

    return user


def check_username(username: str):
    session = create_session()
    user = session.query(User).filter(User.username == username).first()
    session.close()

    return user


def update_username(address: str, username: str):
    session = create_session()
    user = session.query(User).filter(User.address == address).first()

    posts = session.query(Post).filter(Post.author == user.username).all()
    for post in posts:
        post.author = username

    tips = session.query(Tip).filter(Tip.sender == user.username).all()
    for tip in tips:
        tip.sender = username

    tips = session.query(Tip).filter(Tip.recipient == user.username).all()
    for tip in tips:
        tip.recipient = username

    user.username = username

    session.commit()
    session.refresh(user)
    session.close()

    return user


def get_post(username: str, post_id: str):
    session = create_session()
    post = (
        session.query(Post)
        .filter(Post.author == username, Post.id == post_id)
        .first()
    )
    session.close()

    return post


def get_user_posts(username: str):
    session = create_session()
    posts = (
        session.query(Post)
        .filter(Post.author == username)
        .order_by(Post.created_at.desc())
        .all()
    )
    session.close()

    return posts


def get_latest_posts():
    session = create_session()
    posts = session.query(Post).order_by(Post.created_at.desc()).all()
    session.close()

    return posts


def new_post(username: str, post_id: str, title: str, content: str):
    session = create_session()
    post = Post(author=username, id=post_id, title=title, content=content)
    session.add(post)
    session.commit()
    session.close()


def update_post(username: str, post_id: str, title: str, content: str):
    session = create_session()
    post = (
        session.query(Post)
        .filter(Post.author == username, Post.id == post_id)
        .first()
    )
    post.title = title
    post.content = content
    session.commit()
    session.close()


def delete_post(username: str, post_id: str):
    session = create_session()
    post = (
        session.query(Post)
        .filter(Post.author == username, Post.id == post_id)
        .first()
    )
    session.delete(post)
    session.commit()
    session.close()


def record_tip(sender: str, recipient: str, amount: str, post_id: str, tx_hash: str):
    session = create_session()
    tip = Tip(
        sender=sender,
        recipient=recipient,
        amount=amount,
        post_id=post_id,
        tx_hash=tx_hash,
    )
    session.add(tip)
    session.commit()
    session.close()


def get_pending_tips(username: str):
    session = create_session()
    tips = (
        session.query(Tip)
        .filter(Tip.recipient == username, Tip.notified == False)
        .all()
    )
    session.close()

    return tips


def get_sent_tips(username: str):
    session = create_session()
    tips = session.query(Tip).filter(Tip.sender == username).all()
    session.close()

    return tips


def get_received_tips(username: str):
    session = create_session()
    tips = session.query(Tip).filter(Tip.recipient == username).all()
    session.close()

    return tips


def mark_notified(tip_id: int):
    session = create_session()
    tip = session.query(Tip).filter(Tip.id == tip_id).first()
    tip.notified = True
    session.commit()
    session.close()
