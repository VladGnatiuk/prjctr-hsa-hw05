from typing import Dict, Any
import json
import asyncio
import aiohttp

# Google Analytics Configuration
GA_MEASUREMENT_ID = "G-XXXXXXXXXX"  # Replace with your GA4 Measurement ID
GA_API_SECRET = "YOUR_API_SECRET"   # Replace with your GA4 API secret

async def send_ga_event(event_name: str, params: Dict[Any, Any] = None):
    """
    Send server-side events to Google Analytics 4 asynchronously
    """
    endpoint = f"https://www.google-analytics.com/mp/collect?measurement_id={GA_MEASUREMENT_ID}&api_secret={GA_API_SECRET}"
    
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
                return response.status == 204
    except Exception as e:
        print(f"Error sending GA event: {str(e)}")
        return False

async def main():
    # Example of sending an event
    success = await send_ga_event("test_event", {
        "event_category": "test",
        "event_label": "console_app"
    })
    print(f"Event sent successfully: {success}")

if __name__ == "__main__":
    asyncio.run(main())
