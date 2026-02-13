from typing import Optional


class Board:
    def __init__(
        self,
        id: int,
        member_id: int,
        title: str,
        content: str,
        views: int,
        likes: int,
        created_at,
        updated_at,
        is_notice: int = 0,
        active: int = 1,
        is_private: int = 0,
        is_inquiry: int = 0,
        video_url: Optional[str] = None,
        external_link: Optional[str] = None,
    ):
        self.id = id
        self.member_id = member_id
        self.title = title
        self.content = content
        self.views = views
        self.likes = likes
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_notice = is_notice
        self.active = active
        self.is_private = is_private
        self.is_inquiry = is_inquiry
        self.video_url = video_url
        self.external_link = external_link

    @classmethod
    def from_db(cls, row: dict):
        if not row:
            return None

        return cls(
            id=row.get("id"),
            member_id=row.get("member_id"),
            title=row.get("title"),
            content=row.get("content"),
            views=row.get("views") or 0,
            likes=row.get("likes") or 0,
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
            is_notice=row.get("is_notice") or 0,
            active=row.get("active") if row.get("active") is not None else 1,
            is_private=row.get("is_private") or 0,
            is_inquiry=row.get("is_inquiry") or 0,
            video_url=row.get("video_url"),
            external_link=row.get("external_link"),
        )
