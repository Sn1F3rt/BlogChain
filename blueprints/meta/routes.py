from . import meta_bp

from flask import render_template

from utils.crud import get_latest_posts


@meta_bp.route("/", methods=["GET"])
def _index():
    posts = get_latest_posts()

    return render_template("meta/index.html", posts=posts)
