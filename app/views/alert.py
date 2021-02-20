from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    session,
    )

# Local imports
from app.modules import google_helper

bp = Blueprint("index", __name__, url_prefix="/")


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        session["email"] = email
        return redirect(google_helper.get_auth_url(email))

    return render_template("index.html")


@bp.route("/oauth_redirect", methods=["GET", "POST"])
def oauth_redirect():
    # Receives access token from Google
    # after the user authenticates and authorize the app
    auth_code = request.args.get("code")
    session["mail_headers"] = google_helper.get_headers(auth_code)

    return redirect(url_for(".subjects"))


@bp.route("/subjects")
def subjects():
    messages = session["mail_headers"]

    return render_template("headers.html", messages=messages)
