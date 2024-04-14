from . import auth_bp

from flask import jsonify, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user, login_user, logout_user

from datetime import datetime

from siwe import generate_nonce, SiweMessage

from factory import w3
from utils.crud import (
    get_user_by_address,
    add_user,
    activate_user,
    check_username,
    update_username,
    get_pending_tips,
    mark_notified,
)
from utils.forms import UsernameForm


@auth_bp.route("/auth/nonce/<address>", methods=["GET"])
def _nonce(address: str):
    address = w3.to_checksum_address(address)
    user = get_user_by_address(address)

    if user:
        return jsonify({"nonce": user.nonce}), 200

    nonce = generate_nonce()

    add_user(address, nonce)

    return jsonify({"nonce": nonce}), 200


@auth_bp.route("/auth/message/<address>", methods=["GET", "POST"])
def _message(address: str):
    address = w3.to_checksum_address(address)
    user = get_user_by_address(address)

    if not user:
        return jsonify({"error": "No nonce found for this address."})

    data = request.get_json()
    domain = data.get("domain")
    statement = data.get("statement")
    origin = data.get("origin")
    version = data.get("version")
    chain_id = data.get("chain_id")
    nonce = data.get("nonce")

    message = SiweMessage(
        message={
            "domain": domain,
            "address": address,
            "statement": statement,
            "uri": origin,
            "version": version,
            "chain_id": chain_id,
            "issued_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "nonce": nonce,
        }
    )

    return jsonify({"message": message.prepare_message()}), 200


@auth_bp.route("/auth/verify/<address>", methods=["POST"])
def _verify(address: str):
    address = w3.to_checksum_address(address)
    user = get_user_by_address(address)

    if not user:
        return jsonify({"error": "No nonce found for this address."})

    data = request.get_json()
    message = data.get("message")
    signature = data.get("signature")

    message = SiweMessage(message=message)

    try:
        message.verify(signature=signature, nonce=user.nonce)

    except Exception as e:
        return jsonify({"error": e.__str__()}), 400

    if not user.active:
        user = activate_user(address)

    login_user(user)
    flash("You have been logged in.", "success")

    tips = get_pending_tips(current_user.username)

    if tips:
        for tip in tips:
            mark_notified(tip.id)
            flash(
                f"You received a tip of {tip.amount} ETH from {tip.sender}.", "info"
            )

    return jsonify({"username": user.username})


@auth_bp.route("/auth/username/", methods=["GET", "POST"])
@login_required
def _username():
    if current_user.username:
        return redirect(url_for("app._index"))

    username_form = UsernameForm()

    if username_form.validate_on_submit():
        if check_username(username_form.username.data):
            flash("Username already taken.", "warning")
            return redirect(url_for("auth._username"))

        update_username(current_user.address, username_form.username.data)

        flash("Username updated successfully.", "success")

        return redirect(url_for("app._index"))

    return render_template("auth/username.html", username_form=username_form)


@auth_bp.route("/auth/logout")
@login_required
def _logout():
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for("meta._index"))


@auth_bp.route("/auth/settings", methods=["GET", "POST"])
@login_required
def _settings():
    username_form = UsernameForm()

    if username_form.validate_on_submit():
        if current_user.username == username_form.username.data:
            flash("Old and new username cannot be the same.", "warning")
            return redirect(url_for("auth._settings"))

        if check_username(username_form.username.data):
            flash("Username already taken.", "warning")
            return redirect(url_for("auth._settings"))

        update_username(current_user.address, username_form.username.data)
        flash("Username updated successfully.", "success")
        return redirect(url_for("auth._settings"))

    return render_template("auth/settings.html", username_form=username_form)
