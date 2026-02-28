from httpx import RequestError
from pydantic import ValidationError
from schemas.request_models import TaxRequest
from schemas.response_models import TaxServiceResponse, GeoData
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

            response.raise_for_status()

            return TaxServiceResponse(**response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 422:
                return TaxServiceResponse(
                    composite_tax_rate=0.0,
                    tax_amount=0.0,
                    total_amount=request_data.subtotal,
                    breakdown=GeoData(state_rate=0.0, county_rate=0.0, city_rate=0.0, special_rates=0.0),
                    jurisdictions=["Outside New York State"]
                )
            print(f"HTTP error: {e.response.status_code} {e.response.text}")
            raise
        except RequestError as e:
            print(f"Request error: {e}")
            raise
        except ValidationError as e:
            print(f"Validation pydantic error: {e}")
            raise

    async def get_tax_responses(self,
                                requests : list[TaxRequest],
                                timeout : float = 5.0) -> list[TaxServiceResponse]:
        try:
            response = await self._http_client.post("/taxes", json={"orders": [req.model_dump() for req in requests]}, timeout=timeout)

            response.raise_for_status()

            data = response.json()
            return [TaxServiceResponse(**item) for item in data["taxes"]]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 422:
                # Return default responses for all requests
                return [
                    TaxServiceResponse(
                        composite_tax_rate=0.0,
                        tax_amount=0.0,
                        total_amount=req.subtotal,
                        breakdown=GeoData(state_rate=0.0, county_rate=0.0, city_rate=0.0, special_rates=0.0),
                        jurisdictions=["Outside New York State"]
                    ) for req in requests
                ]
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
