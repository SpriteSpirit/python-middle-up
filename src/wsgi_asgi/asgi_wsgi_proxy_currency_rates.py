import logging

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()


@app.get("/{currency}")
async def get_exchange_rate(currency: str) -> dict:
    """
    Возвращает курс валюты в формате JSON.

    :param currency: Идентификатор валюты (например, USD, EUR, GBP).
    :return: Курс валюты в виде JSON-объекта.
    """

    # URL API (используется v4, так как он бесплатный)
    url = f"https://api.exchangerate-api.com/v4/latest/{currency}"

    logging.debug(f"Requesting URL: {url}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            logging.debug(f"Response status: {response.status_code}")

            # Если запрос неудачный, выбрасываем исключение
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка получения обменного курса",
                )

            data = response.json()

            return {
                "provider": "www.exchangerate-api.com",
                "WARNING_UPGRADE_TO_V6": "https://www.exchangerate-api.com/docs/free",
                "terms": "https://www.exchangerate-api.com/terms",
                "base": data["base"],
                "date": data["date"],
                "time_last_updated": data["time_last_updated"],
                "rates": data["rates"],
            }

        except httpx.RequestError as e:
            logging.error(f"Network error: {e}")
            raise HTTPException(status_code=500, detail="Ошибка сети при запросе к API")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
