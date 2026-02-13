from lms.repositories.admin_repo import AdminRepo

class AdminService:

    @staticmethod
    def get_dashboard_stats():
        member_stats = AdminRepo.get_member_stats()

        # 🔽 여기서 비즈니스 로직 추가 가능
        if not member_stats:
            member_stats = {
                "total": 0,
                "active": 0,
                "blocked": 0,
                "new_30d": 0
            }

        return {"student": member_stats}
