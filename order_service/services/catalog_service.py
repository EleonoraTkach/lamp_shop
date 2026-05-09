import httpx
import os

class CatalogClient:
    def __init__(self):
        self.base_url = os.getenv("CATALOG_URL", "http://catalog_service:8000")

    async def get_product(self, product_id: int) -> bool:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/products/{product_id}"
            )

            if resp.status_code == 404:
                return None

            resp.raise_for_status()
            return resp.json()

    async def update_quantity(self, product_id: int, new_quantity: int):
        async with httpx.AsyncClient() as client:
            resp = await client.patch(
                f"{self.base_url}/products/{product_id}",json={"quantity": new_quantity}
            )

            resp.raise_for_status()
            return True