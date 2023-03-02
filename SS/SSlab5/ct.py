import asyncio
import pandas as pd
import aiohttp
from typing import Coroutine, Tuple, Optional
import os
import json
import random
from bs4 import BeautifulSoup


async def check_ct(name: str, *, sem : asyncio.Semaphore) -> bool:
    async with aiohttp.ClientSession() as session:
        while True:
            await sem.acquire()
            async with session.get(url=f"https://crt.sh/?dNSName={name}&match==") as response:
                sem.release()
                if response.status == 429:
                    print("Too many requests, waiting")
                    await asyncio.sleep(random.uniform(1.0, 3.0))
                    continue
                res_text = await response.text()
                soup = BeautifulSoup(res_text, "html.parser")
                certs = soup.select_one(
                    "body > table:nth-child(8) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)")
                if certs is None:
                    return True
                return certs.text != "None found"


async def main():
    df = pd.read_csv("200_hsts.csv")
    reachable_domains = df.copy()[df["HSTS?"].notna()]
    sem = asyncio.Semaphore(5)
    results = await asyncio.gather(
        *[check_ct(name, sem=sem) for name in reachable_domains["Domain"]]
    )
    reachable_domains["CT?"] = results
    reachable_domains.to_csv("200_ct.csv", index=None, header=True)
    df.join(reachable_domains.drop(["Domain", "HSTS?"], axis=1).set_index("S/N"), on="S/N")
    df.to_csv("200_ct_combined.csv", index=None, header=True)


if __name__ == "__main__":
    asyncio.run(main())
