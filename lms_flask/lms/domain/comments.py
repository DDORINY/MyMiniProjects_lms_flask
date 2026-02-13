# 댓글과 대댓글 테이블 객체화
class Comments:
    def __init__(
            self,
            id:int,
            board_id:int,
            member_id:int,
            parent_id:int,
            comment:str,
            created_at):

        self.id = id
        self.board_id = board_id
        self.member_id = member_id
        self.parent_id = parent_id
        self.comment = comment
        self.created_at = created_at
