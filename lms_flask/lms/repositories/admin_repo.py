
from lms.common.db import get_connection

class AdminRepo:

    @staticmethod
    def get_member_stats():
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                        SELECT
                          COUNT(*) AS total,
                          SUM(active=1) AS active,
                          SUM(active=0) AS blocked,
                          SUM(created_at >= NOW() - INTERVAL 30 DAY) AS new_30d
                        FROM members
                    """)
                return cur.fetchone()
        finally:
            conn.close()


