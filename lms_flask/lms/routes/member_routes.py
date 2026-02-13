# routes/member_routes.py
import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename

from lms.common.auth import Auth
from lms.service.AuthService import AuthService
from lms.service.MemberService import MemberService

bp = Blueprint("member", __name__)

# ----------------------------
# Upload 설정 (프로필)
# ----------------------------
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

def get_profile_upload_dir() -> str:
    """
    static/uploads/profile
    """
    base_dir = current_app.root_path  # lms_flask/
    upload_dir = os.path.join(base_dir, "static", "uploads", "profile")
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir


# ----------------------------
# Auth (Login/Logout)
# ----------------------------
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("member/login.html")

    uid = request.form.get("uid", "")
    pw = request.form.get("pw", "")

    try:
        member = AuthService.login(uid, pw)

        # 세션 표준 키
        session["user_id"] = member.id
        session["user_uid"] = member.uid
        session["user_name"] = member.name
        session["email"] = member.email
        session["role"] = member.role
        session["profile_img"] = member.profile_img

        flash("로그인되었습니다.")
        return redirect(url_for("main.index"))

    except ValueError as e:
        flash(str(e))
        return redirect(url_for("member.login"))
    except Exception as e:
        flash(f"서버 오류: {e}")
        return redirect(url_for("member.login"))


@bp.route("/logout")
def logout():
    session.clear()
    flash("로그아웃되었습니다.")
    return redirect(url_for("main.index"))


# ----------------------------
# Join
# ----------------------------
@bp.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "GET":
        return render_template("member/join.html")

    uid = request.form.get("uid", "")
    password = request.form.get("password", "")
    name = request.form.get("name", "")
    email = request.form.get("email", "").strip() or None  # 템플릿에서 없으면 "" 들어옴

    try:
        member = MemberService.join(uid, password, name, email=email or None)

        # 가입 후 자동 로그인
        session["user_id"] = member.id
        session["user_uid"] = member.uid
        session["user_name"] = member.name
        session["email"] = member.email
        session["role"] = member.role
        session["profile_img"] = member.profile_img

        flash("회원가입 + 자동 로그인 완료")
        return redirect(url_for("main.index"))

    except ValueError as e:
        flash(str(e))
        return redirect(url_for("member.join"))
    except Exception as e:
        flash(f"서버 오류: {e}")
        return redirect(url_for("member.join"))


# ----------------------------
# My Page
# ----------------------------
@bp.route("/mypage")
def mypage():
    if not Auth.is_login():
        return redirect(url_for("member.login"))

    try:
        member = MemberService.get_my_page(session["user_id"])
        return render_template("member/mypage.html", user=member)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("main.index"))


# ----------------------------
# Member Edit
# ----------------------------
@bp.route("/member/edit", methods=["GET", "POST"])
def member_edit():
    if not Auth.is_login():
        return redirect(url_for("member.login"))

    if request.method == "GET":
        member = MemberService.get_my_page(session["user_id"])
        return render_template("member/edit.html", user=member)

    name = request.form.get("name", "")
    email = request.form.get("email", "")
    pw = request.form.get("password", "")

    try:
        MemberService.edit_profile(
            member_id=session["user_id"],
            name=name,
            email=email or None,
            password=pw or None
        )

        # 세션 갱신(화면 즉시 반영)
        session["user_name"] = name.strip()

        flash("회원정보가 수정되었습니다.")
        return redirect(url_for("member.mypage"))

    except ValueError as e:
        flash(str(e))
        return redirect(url_for("member.member_edit"))


# ----------------------------
# Member Delete (Soft Delete)
# ----------------------------
@bp.route("/member/delete", methods=["POST"])
def member_delete():
    if not Auth.is_login():
        return redirect(url_for("member.login"))

    pw = request.form.get("password", "")

    try:
        MemberService.delete_member(session["user_id"], pw)
        session.clear()
        flash("회원탈퇴되었습니다.")
        return redirect(url_for("main.index"))

    except ValueError as e:
        flash(str(e))
        return redirect(url_for("member.member_edit"))


# ----------------------------
# Profile Upload
# ----------------------------
@bp.route("/member/profile", methods=["POST"])
def upload_profile():
    if not Auth.is_login():
        return redirect(url_for("member.login"))

    file = request.files.get("profile")
    if not file or file.filename == "":
        flash("업로드할 파일을 선택해주세요.")
        return redirect(url_for("member.mypage"))

    if not allowed_file(file.filename):
        flash("이미지 파일만 업로드 가능합니다. (png/jpg/jpeg/gif/webp)")
        return redirect(url_for("member.mypage"))

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filename = secure_filename(filename)

    upload_dir = get_profile_upload_dir()
    save_path = os.path.join(upload_dir, filename)

    # 기존 파일 삭제(세션에 파일명 저장된 경우)
    old = session.get("profile_img")
    if old:
        old_path = os.path.join(upload_dir, old)
        if os.path.exists(old_path):
            os.remove(old_path)

    file.save(save_path)

    try:
        MemberService.update_profile_img(session["user_id"], filename)
        session["profile_img"] = filename
        flash("프로필 이미지가 등록되었습니다.")
    except ValueError as e:
        # 저장 실패 시 업로드 파일도 정리(선택)
        if os.path.exists(save_path):
            os.remove(save_path)
        flash(str(e))

    return redirect(url_for("member.mypage"))


