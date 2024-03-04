from pydantic import BaseModel


class IVote(BaseModel):
    post_id: int
    is_voted: bool
