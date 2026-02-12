from typing import Optional, List
from common.db import get_connection
from domain.Member import Member

class MemberRepo:
# [v] find_by_uid(uid) (로그인)
# [v] find_by_id(member_id) (마이페이지/상세)
# [v] exists_uid(uid) (가입 중복체크)
# [v] insert_member(uid, password, name, email=None, role='user') -> new_id (가입)
# [v] update_member(member_id, name, email=None, password=None) (수정)
# [v] set_profile_img(member_id, filename) (프로필)
# [v] set_active(member_id, active) (탈퇴/블랙리스트/복구)
# [v] list_members(active=None) (관리자 목록: 활성/비활성 분리)

    @staticmethod
    # [v] find_by_uid(uid) (로그인: active=1 사용자만)
    def find_by_uid(uid: str) -> Optional[Member]:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                        SELECT *
                        FROM members
                        WHERE uid = %s
                        LIMIT 1
                        """
                cursor.execute(sql, (uid,))
                row = cursor.fetchone()
                return Member.from_db(row)
        finally:
            conn.close()

    # [v] find_by_id(member_id) (마이페이지/상세: active 상관없이 조회 가능하게)
    @staticmethod
    def find_by_id(member_id:int) -> Optional[Member]:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                SELECT *
                FROM members
                WHERE id = %s
                LIMIT 1
                """
                cursor.execute(sql, (member_id,))
                row = cursor.fetchone()
                return Member.from_db(row)
        finally:
            conn.close()

    # [v] exists_uid(uid) (가입 중복체크: active 상관없이 uid는 유니크라 존재 여부만)
    @staticmethod
    def exists_uid(uid:str) -> bool:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                SELECT 1 
                FROM members 
                WHERE uid = %s 
                LIMIT 1
                """
                cursor.execute(sql, (uid,))
                row = cursor.fetchone()
                return row is not None

        finally:
            conn.close()

    # [v] insert_member(uid, password, name, email=None, role='user') -> new_id
    @staticmethod
    def insert_member(uid:str, password:str, name:str, email=None, role='user') -> int:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO members(uid,password,name,email,role,active) 
                VALUES(%s,%s,%s,%s,%s,1)
                """
                cursor.execute(sql, (uid, password, name, email, role))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    # [v] update_member(member_id, name, email=None, password=None)
    @staticmethod
    def update_member(member_id:int, name:str,
                      email: Optional[str] = None, password: Optional[str] = None) -> None:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                if password:
                    sql = """
                    UPDATE members 
                    SET name = %s, email = %s, password = %s 
                    WHERE id = %s 
                    """
                    cursor.execute(sql, (name, email, password, member_id))
                else:
                    sql = """
                    UPDATE members 
                    SET name = %s, email = %s
                    WHERE id = %s 
                    """
                    cursor.execute(sql, (name, email, member_id, ))
            conn.commit()
        finally:
            conn.close()
    # [v] set_profile_img(member_id, filename) (프로필)
    @staticmethod
    def set_profile_img(member_id:int, filename: str) -> None:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql="""
                UPDATE members 
                SET profile_img = %s 
                WHERE id = %s 
                """
                cursor.execute(sql, (filename, member_id))
            conn.commit()
        finally:
            conn.close()

    # [v] set_active(member_id, active) (탈퇴/블랙리스트/복구)
    @staticmethod
    def set_active(member_id:int,active: bool) -> None:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                UPDATE members 
                SET active = %s
                WHERE id = %s
                """
                cursor.execute(sql, (1 if active else 0, member_id))
            conn.commit()
        finally:
            conn.close()

    # [v] list_members(active=None) (관리자 목록: 활성/비활성 분리)
    @staticmethod
    def list_members(active: Optional[bool] = None) -> List[Member]:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                if active is None:
                    sql = """
                    SELECT *
                    FROM members
                    ORDER BY id DESC"""
                    cursor.execute(sql)
                else:
                    sql = """
                    SELECT *
                    FROM members
                    WHERE active = %s
                    ORDER BY id DESC
                    """
                    cursor.execute(sql, (1 if active else 0,))
                rows = cursor.fetchall()
                return [Member.from_db(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def update_last_login(member_id: int) -> None:
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                UPDATE members
                SET last_login_at = NOW()
                WHERE id = %s
                """
                cursor.execute(sql, (member_id,))
            conn.commit()
        finally:
            conn.close()

