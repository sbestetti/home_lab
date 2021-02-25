import json
from flask import (
    Blueprint,
    render_template,
    redirect,
    jsonify,
    request,
    session,
    )
from flask.helpers import url_for

# Local imports
from app.modules import google_helper

bp = Blueprint("alert", __name__, url_prefix="/alert")


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        session["email"] = email
        return redirect(google_helper.get_auth_url(email))

    return render_template("index.html")


@bp.route("/watch", methods=["GET", "POST"])
def watch():
    if request.method == "POST":
        email = request.form.get("email")
        session["email"] = email
        return redirect(google_helper.get_auth_url(email))

    return render_template("index.html")


@bp.route("/oauth_redirect", methods=["GET", "POST"])
def oauth_redirect():
    '''
    Receives access token from Google
    after the user authenticates and authorize the app
    '''
    session["auth_code"] = request.args.get("code")
    return redirect(url_for("alert.dashboard"))


@bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    raw_labels = google_helper.get_labels(session["auth_code"])
    labels = list()
    for label in raw_labels["labels"]:
        if label["type"] == "user":
            labels.append(label["name"])
    return jsonify(labels)


@bp.route("/subjects")
def subjects():
    messages = session["mail_headers"]

    return render_template("headers.html", messages=messages)


@bp.route("/inbound", methods=["POST"])
def alerts():
    envelope = json.loads(request.data.decode("utf-8"))
    # payload = base64.b64decode(envelope["message"]["data"])
    # print(payload)
    print(envelope)
    return "", 204
