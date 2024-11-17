from typing import Optional
import httpx
from api.internalApi.user_service.model.user_response import UserResponse
from config.config import Config

config = Config()


async def get_user_by_id(user_id: int) -> Optional[UserResponse]:
    url = f"{config.USER_SERVICE_BASE_URL}/user/{user_id}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()

            data = response.json()

            user_response = UserResponse(**data)

            return user_response
        except httpx.HTTPStatusError as exception:
            print(f"Error in getting item details for item id {user_id} with error: {exception.response}")
            return None
