from . import posts_bp

from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required

import secrets

from utils.forms import PostForm
from utils.crud import get_post, get_user_posts, new_post, update_post, delete_post


@posts_bp.route("/posts/me", methods=["GET"])
@login_required
def _me():
    posts = get_user_posts(current_user.username)

    return render_template("posts/me.html", posts=posts)


@posts_bp.route("/posts/view/<author>/<post_id>", methods=["GET"])
def _view(author: str, post_id: str):
    post = get_post(author, post_id)

    if not post:
        flash("Post not found.", "error")
        return redirect(url_for("meta._index"))

    return render_template("posts/view.html", post=post)


@posts_bp.route("/posts/new", methods=["GET", "POST"])
@login_required
def _new():
    post_form = PostForm()

    if post_form.validate_on_submit():
        post_id = secrets.token_hex(4)
        new_post(
            current_user.username,
            post_id,
            post_form.title.data,
            post_form.content.data,
        )

        flash("Post created.", "success")
        return redirect(url_for("posts._me"))

    return render_template("posts/new.html", post_form=post_form)


@posts_bp.route("/posts/update/<author>/<post_id>", methods=["GET", "POST"])
@login_required
def _update(author: str, post_id: str):
    post = get_post(author, post_id)

    if not post:
        flash("Post not found.", "error")
        return redirect(url_for("posts._me"))

    post_form = PostForm()

    if post_form.validate_on_submit():
        update_post(author, post_id, post_form.title.data, post_form.content.data)

        flash("Post updated.", "success")
        return redirect(url_for("posts._view", author=author, post_id=post_id))

    post_form.title.data = post.title
    post_form.content.data = post.content

    return render_template("posts/update.html", post_id=post.id, post_form=post_form)


@posts_bp.route("/posts/delete/<author>/<post_id>", methods=["GET"])
@login_required
def _delete(author: str, post_id: str):
    post = get_post(author, post_id)

    if not post:
        flash("Post not found.", "error")
        return redirect(url_for("posts._me"))

    delete_post(author, post_id)

    flash("Post deleted.", "success")
    return redirect(url_for("posts._me"))
