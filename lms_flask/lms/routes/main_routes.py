# routes/main_routes.py
from flask import Blueprint, render_template

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    # templates/main.html 사용 (없으면 원하는 파일명으로 변경)
    return render_template("main.html")
