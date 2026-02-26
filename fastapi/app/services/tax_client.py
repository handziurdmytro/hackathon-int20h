from pydantic import ValidationError
from urllib3.exceptions import RequestError

from schemas.request_models import TaxRequest
from schemas.response_models import TaxServiceResponse
import httpx

class TaxServiceClient:

    def __init__(self, url: str):
        self._url = url
        self._http_client = httpx.AsyncClient(base_url=self._url)

    async def get_tax_response(self,
                               request_data : TaxRequest,
                               timeout : float = 5.0) -> TaxServiceResponse | None:
        try:
            response = await self._http_client.post("/tax", json=request_data.model_dump(), timeout=timeout)

            response.raise_for_status() # Якщо статус код не 2xx, викликає виняток і ми його ловим

            return TaxServiceResponse(**response.json())
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} {e.response.text}")
            raise
        except RequestError as e:
            print(f"Request error: {e}")
            raise
        except ValidationError as e:
            print(f"Validation pydantic error: {e}")
            raise


    async def close(self):
        await self._http_client.aclose()
