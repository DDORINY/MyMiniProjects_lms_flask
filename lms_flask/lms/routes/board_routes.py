
from flask import Blueprint

bp = Blueprint("board", __name__)

@bp.route("/board")
def board_list():
    return "게시판 목록(임시)"
