from typing import List

from app.schemas.entities.user import UserModel
from app.schemas.response.success import SuccessResponse


class ListUserResponse(SuccessResponse[List[UserModel]]):
    pass
