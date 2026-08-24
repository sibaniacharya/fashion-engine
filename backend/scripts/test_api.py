import httpx
import asyncio

async def test_endpoints():
    base_url = "http://127.0.0.1:8000/api"
    endpoints = [
        "/dashboard",
        "/themes",
        "/opportunities",
        "/wishlist-behavior",
        "/purchase-barriers",
        "/segments",
        "/sources",
        "/external-research",
        "/evidence",
        "/data-quality",
        "/health"
    ]
    
    async with httpx.AsyncClient() as client:
        for ep in endpoints:
            url = f"{base_url}{ep}"
            try:
                response = await client.get(url, timeout=5.0)
                if response.status_code == 200:
                    print(f"PASS: {ep}")
                else:
                    print(f"FAIL: {ep} - Status: {response.status_code}")
                    print(response.json())
            except Exception as e:
                print(f"ERROR: {ep} - {e}")

if __name__ == "__main__":
    asyncio.run(test_endpoints())
