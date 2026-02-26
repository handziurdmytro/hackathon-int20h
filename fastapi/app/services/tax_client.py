from schemas.request_models import TaxRequest
from schemas.response_models import TaxServiceResponse
import httpx

class TaxServiceClient:

    def __init__(self, url: str):
        self._url = url

    async def get_tax_response(self, request_data : TaxRequest, timeout : float = 5.0) -> TaxServiceResponse:
        async with httpx.AsyncClient(base_url=self._url) as client:
            response = await client.post("/tax", json=request_data.model_dump(), timeout=timeout)
            return TaxServiceResponse(**response.json())
