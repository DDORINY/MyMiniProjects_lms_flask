class Member:

    def __init__(self,id,uid,password,name,email,role="user",active=True, profile_img=None,created_at=None):
        self.id = id
        self.uid = uid
        self.password = password
        self.name = name
        self.email = email
        self.role = role
        self.active = active
        self.profile_img = profile_img
        self.created_at = created_at


    @classmethod
    def from_db(cls,row:dict):
        if not row:
            return None

        return cls(
            id = row.get('id'),
            uid = row.get('uid'),
            password = row.get('password'),
            name = row.get('name'),
            email = row.get('email'),
            role = row.get('role'),
            active = bool(row.get('active')),
            profile_img = row.get('profile_img'),
            created_at=row.get("created_at")
        )