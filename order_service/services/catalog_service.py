import httpx
import os

class CatalogClient:
    def __init__(self):
        self.base_url = os.getenv("CATALOG_URL", "http://catalog_service:8000") # внутри docker сети

    async def product_exists(self, product_id: int) -> bool:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/products/{product_id}"
            )

            if resp.status_code == 404:
                return False

            resp.raise_for_status()
            return True