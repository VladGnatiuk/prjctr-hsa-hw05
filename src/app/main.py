from typing import Dict, Any
import json
import asyncio
import aiohttp
import os
from datetime import datetime

# Get Google Analytics Configuration from environment variables
GA_MEASUREMENT_ID = os.getenv('GA_MEASUREMENT_ID')
GA_API_SECRET = os.getenv('GA_API_SECRET')

if not GA_MEASUREMENT_ID or not GA_API_SECRET:
    raise ValueError("GA_MEASUREMENT_ID and GA_API_SECRET environment variables must be set")

async def send_ga_event(
    event_name: str, 
    params: Dict[Any, Any] = None
):
    """
    Send server-side events to Google Analytics 4 asynchronously
    """
    endpoint = f"https://www.google-analytics.com/mp/collect?measurement_id={GA_MEASUREMENT_ID}&api_secret={GA_API_SECRET}"
    # endpoint = f"https://www.google-analytics.com/debug/mp/collect?measurement_id={GA_MEASUREMENT_ID}&api_secret={GA_API_SECRET}"
    
    payload = {
        "client_id": "server-side-client",
        "events": [{
            "name": event_name,
            "params": params or {}
        }]
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=payload) as response:
                content = await response.text()
                print(f"Response content: {content}")
                return response.status == 204
    except Exception as e:
        print(f"Error sending GA event: {str(e)}")
        return False


async def get_exchange_rate(valcode: str) -> Dict[str, Any]:
    today = datetime.now().strftime("%Y%m%d")
    endpoint = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json&valcode={valcode}&date={today}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    return data[0]
    except Exception as e:
        print(f"Error fetching exchange rate: {str(e)}")
        return None


async def periodic_rate_check():
    while True:
        rate_data = await get_exchange_rate('USD')
        print(rate_data)
        await send_ga_event("exchange_rate_fetch", rate_data)
        
        # await asyncio.sleep(3600)  # Sleep for 1 hour
        await asyncio.sleep(60)  # Sleep for 1 minute


async def main():
    # await send_ga_event("test_event", {
    #     "event_category": "test",
    #     "event_label": "console_app"
    # })
    tasks = [
        asyncio.create_task(periodic_rate_check()),
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
