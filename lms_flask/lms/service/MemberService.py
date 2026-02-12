from typing import Optional, List
from repositories.member_repo import MemberRepo
from domain.Member import Member

class MemberService:

    # 회원가입
    @staticmethod
    def join(uid:str, password:str,name:str,
             email: Optional[str] = None, role: str = "user"):
        uid = (uid or "").strip()
        password = (password or "").strip()
        name = (name or "").strip()
        email = (email or "").strip() if email else None

        if not uid or not password or not name:
            raise ValueError("아이디/비밀번호/이름은 필수입니다.")

        #uid 중복체크
        if MemberRepo.exists_uid(uid):
            raise ValueError("중복된 아이디입니다.")

        new_id =MemberRepo.insert_member(uid, password, name, email, role)

        # 생성된 회원 조회에서 반환(일관성)
        member = MemberRepo.find_by_id(new_id)
        if not member:
            raise ValueError("회원가입이 실패했습니다.")
        return member

    @staticmethod
    def get_my_page(member_id: int) -> Member:
        """마이페이지: 내 정보 조회"""
        member = MemberRepo.find_by_id(member_id)
        if not member:
            raise ValueError("회원 정보를 찾을 수 없습니다.")
        if not member.active:
            # 로그인 상태인데 비활성일 수 있는 케이스 방어(관리자가 비활성 처리 등)
            raise ValueError("비활성화 계정입니다.")
        return member

    @staticmethod
    def edit_profile(member_id: int, name: str,
                     email: Optional[str] = None,
                     password: Optional[str] = None) -> None:
        """회원정보 수정"""
        name = (name or "").strip()
        email = (email or "").strip() if email else None
        password = (password or "").strip() if password else None

        if not name:
            raise ValueError("이름은 필수입니다.")

        member = MemberRepo.find_by_id(member_id)
        if not member:
            raise ValueError("회원 정보를 찾을 수 없습니다.")
        if not member.active:
            raise ValueError("비활성화 계정은 수정할 수 없습니다.")

        MemberRepo.update_member(member_id, name, email, password)

    @staticmethod
    def update_profile_img(member_id: int, filename: str) -> None:
        """프로필 이미지 파일명 저장"""
        filename = (filename or "").strip()
        if not filename:
            raise ValueError("파일명이 비어있습니다.")

        member = MemberRepo.find_by_id(member_id)
        if not member:
            raise ValueError("회원 정보를 찾을 수 없습니다.")
        if not member.active:
            raise ValueError("비활성화 계정은 변경할 수 없습니다.")

        MemberRepo.set_profile_img(member_id, filename)

    @staticmethod
    def delete_member(member_id: int, password: str) -> None:
        """
        회원탈퇴(soft delete)
        - 비밀번호 확인 후 active=0 처리
        """
        password = (password or "").strip()
        if not password:
            raise ValueError("비밀번호를 입력해주세요.")

        member = MemberRepo.find_by_id(member_id)
        if not member:
            raise ValueError("회원 정보를 찾을 수 없습니다.")
        if not member.active:
            raise ValueError("이미 탈퇴(비활성)된 회원입니다.")

        if member.password != password:
            raise ValueError("비밀번호가 일치하지 않습니다.")

        MemberRepo.set_active(member_id, False)

    # ----------------------------
    # ADMIN
    # ----------------------------

    @staticmethod
    def list_members(active: Optional[bool] = None) -> List[Member]:
        """
        관리자 회원 목록
        - active=None: 전체
        - active=True: 활성
        - active=False: 비활성(블랙리스트)
        """
        return MemberRepo.list_members(active)

    @staticmethod
    def get_member_detail(member_id: int) -> Member:
        """관리자 회원 상세"""
        member = MemberRepo.find_by_id(member_id)
        if not member:
            raise ValueError("회원 정보를 찾을 수 없습니다.")
        return member

    @staticmethod
    def set_blacklist(member_id: int, active: bool) -> None:
        """
        관리자: 블랙리스트/복구
        - active=False: 비활성(블랙리스트)
        - active=True: 복구
        """
        member = MemberRepo.find_by_id(member_id)
        if not member:
            raise ValueError("회원 정보를 찾을 수 없습니다.")

        MemberRepo.set_active(member_id, active)