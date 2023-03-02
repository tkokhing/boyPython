import asyncio
import pandas as pd
import aiohttp
from typing import Coroutine, Tuple, Optional


async def check_hsts(name: str) -> Optional[bool]:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
        try:
            async with session.head(url=f"http://{name}", allow_redirects=True) as response:
                return "Strict-Transport-Security" in response.headers
        except aiohttp.ClientError as _:
            return None
        except asyncio.exceptions.TimeoutError as _:
            return None


async def main():
    df = pd.read_csv("200.csv")
    results = await asyncio.gather(
        *[check_hsts(name) for name in df["Domain"]]
    )
    df["HSTS?"] = results
    df.to_csv("200_hsts.csv", index=None, header=True)

if __name__ == "__main__":
    asyncio.run(main())