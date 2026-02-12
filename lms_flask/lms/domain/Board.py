class Board:
    def __init__(self, id:int, member_id:int, title:str, content:str, created_at):
        self.id = id
        self.member_id = member_id
        self.title = title
        self.content = content
        self.created_at = created_at

    @classmethod
    def from_db(cls,row:dict):
        if not row:
            return None

        return cls(
            id = row.get('id'),
            member_id = row.get('member_id'),
            title = row.get('title'),
            content = row.get('content'),
            created_at = row.get('created_at')
        )