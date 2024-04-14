from . import tips_bp

from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from utils.forms import TipForm
from utils.crud import (
    get_post,
    get_user_by_address,
    get_user_by_username,
    record_tip,
    get_sent_tips,
    get_received_tips,
)


@tips_bp.route("/tips/send/<author>/<post_id>", methods=["GET"])
@login_required
def _send(author: str, post_id: str):
    post = get_post(author, post_id)

    if not post:
        flash("Post not found.", "danger")
        return redirect(url_for("meta._index"))

    if author == current_user.username:
        flash("You can't tip your own post.", "danger")
        return redirect(url_for("posts._view", author=author, post_id=post_id))

    user = get_user_by_username(author)

    tip_form = TipForm()
    tip_form.sender.data = current_user.address
    tip_form.sender.render_kw = {"readonly": True}
    tip_form.recipient.data = user.address
    tip_form.recipient.render_kw = {"readonly": True}

    return render_template("tips/send.html", post=post, tip_form=tip_form)


@tips_bp.route("/tips/record", methods=["POST"])
@login_required
def _record():
    data = request.get_json()
    sender = data.get("sender")
    recipient = data.get("recipient")
    amount = data.get("amount")
    post_id = data.get("post_id")
    tx_hash = data.get("txHash")

    username = get_user_by_address(sender).username
    recipient = get_user_by_address(recipient).username

    record_tip(username, recipient, amount, post_id, tx_hash)

    return jsonify({"success": "Tip recorded."}), 200


@tips_bp.route("/tips/view", methods=["GET"])
@login_required
def _view():
    sent_tips = get_sent_tips(current_user.username)
    received_tips = get_received_tips(current_user.username)

    return render_template(
        "tips/view.html", sent_tips=sent_tips, received_tips=received_tips
    )
