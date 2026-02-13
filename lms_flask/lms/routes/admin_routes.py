from flask import Blueprint, redirect, url_for, render_template, flash
from lms.common.auth import Auth
from lms.service.AdminService import AdminService
from lms.service.MemberService import MemberService

bp = Blueprint("admin", __name__)

def admin_guard():
    if not Auth.is_login() or not Auth.is_admin():
        flash("권한이 없습니다.")
        return False
    return True

@bp.route("/dashboard")
def dashboard():
    if not admin_guard():
        return redirect(url_for("member.login"))
    stats = AdminService.get_dashboard_stats()
    return render_template("admin/admin_main.html", stats=stats)

@bp.route("/members")
def members_list():
    if not admin_guard():
        return redirect(url_for("main.index"))
    members = MemberService.list_members(active=None)
    return render_template("admin/members_list.html", members=members, mode="all")

@bp.route("/members/active")
def members_active():
    if not admin_guard():
        return redirect(url_for("main.index"))
    members = MemberService.list_members(active=True)
    return render_template("admin/members_list.html", members=members, mode="active")

@bp.route("/members/inactive")
def members_inactive():
    if not admin_guard():
        return redirect(url_for("main.index"))
    members = MemberService.list_members(active=False)
    return render_template("admin/members_list.html", members=members, mode="inactive")
# ----------------------------
# Dummy Pages (placeholder)
# 템플릿 url_for 에러 방지용
# ----------------------------

@bp.route("/professors")
def professors_list():
    if not admin_guard():
        return redirect(url_for("main.index"))
    return "<h3>교수 목록 (준비중)</h3>"


@bp.route("/professors/by-lecture")
def professor_by_lecture():
    if not admin_guard():
        return redirect(url_for("main.index"))
    return "<h3>강의별 담당 교수 (준비중)</h3>"


@bp.route("/professors/popular")
def professor_popular():
    if not admin_guard():
        return redirect(url_for("main.index"))
    return "<h3>인기 교수 (준비중)</h3>"


@bp.route("/lectures")
def lectures_list():
    if not admin_guard():
        return redirect(url_for("main.index"))
    return "<h3>강의 목록 (준비중)</h3>"


@bp.route("/scores")
def scores_overview():
    if not admin_guard():
        return redirect(url_for("main.index"))
    return "<h3>성적 개요 (준비중)</h3>"

