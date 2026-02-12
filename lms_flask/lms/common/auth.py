from flask import session

class Auth:

    @staticmethod
    def is_login():
        return "user_id" in session

    @staticmethod
    def is_admin():
        return session.get('role') == "admin"

