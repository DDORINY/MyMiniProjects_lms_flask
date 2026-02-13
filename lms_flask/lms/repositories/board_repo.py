from lms.common.db import get_connection
from typing import Optional, List, Dict, Any, Tuple

#<최종 목표>
# [] : 게시글 작성
# [] : 게시글 조회 /공지는 최상단 배치
# [] : 게시글 수정
# [] : 게시글 삭제 (비활성화/비공개)
# [] : 회원 게시글 목록 게시판 (조회/수정/비공개/삭제)
# [] : 게시판 글+이미지+링크(영상연동)+첨부파일
# [] : 공지생성(관리자와 교수 계정만 사용가능)
# [] : 관리자는 게시물 비활성화 처리 가능
# [] : 금지어 정해서 금지어가 있는 경우 자동 비활성화
# [] : 문의 게시판
# [] : 답변 : 관리자와 회원(작성자)만 볼 수 있음 /문의게시판은 별도 페이지 제작
# [] : 댓글과 대댓글 작업
# [] : 인기 게시글 공지 아래 [HOT] 아이콘과 함께(조회수가 높고 좋아요가 많은 경우 상단 배치 3개까지 가능)
# [] : 페이징 15개 게시글


# BoardRepo 목록/상세/작성/수정/비활성/조회수증가/공지세팅/HOT쿼리/내글목록
class BoardRepo:
    # LIST (공지 상단 + HOT 3개 + 최신글, 댓글수 포함)
    @staticmethod
    def list_posts():pass


    @staticmethod
    def count_posts():pass

    @staticmethod
    def increase_views():pass

    # -----------------------------------------
    # CREATE
    # -----------------------------------------
    @staticmethod
    def insert_post():pass

    # -----------------------------------------
    # UPDATE
    # -----------------------------------------
    @staticmethod
    def update_post():pass

    # -----------------------------------------
    # SOFT DELETE / ADMIN DISABLE
    # -----------------------------------------
    @staticmethod
    def set_active():pass

    @staticmethod
    def set_notice():pass

    # -----------------------------------------
    # MY POSTS
    # -----------------------------------------
    @staticmethod
    def list_by_member():pass

    # -----------------------------------------
    # DETAIL
    # -----------------------------------------
    @staticmethod
    def get_post():pass
