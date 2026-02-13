from lms.repositories.member_repo import MemberRepo

class AuthService:
    @staticmethod
    def login(uid:str, password:str):
        uid = (uid or "").strip()
        password = (password or "").strip()

        if not uid or not password:
            raise ValueError("아이디와 비밀번호를 입력해주세요.")

        member = MemberRepo.find_by_uid(uid)

        if not member:
            raise ValueError("아이디가 맞지 않습니다.")

        if not member.active:
            raise ValueError("비활성화 계정입니다.")

        if member.password != password:
            raise ValueError("비밀번호가 맞지 않습니다.")

        MemberRepo.update_last_login(member.id)

        return member

