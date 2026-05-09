import httpx
import os

class OrderClient:
    def __init__(self):
        self.base_url = os.getenv("ORDER_URL", "http://order_service:8001")


    async def order_exists(self, order_num: str) -> bool:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/orders/track/{order_num}"
            )

            if resp.status_code == 404:
                return False

            resp.raise_for_status()
            return True