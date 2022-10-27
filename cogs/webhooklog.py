import aiohttp
import os

logwebhook = os.environ['logwebhook']

async def webhooklog(msg):
  async with aiohttp.ClientSession() as session:
    async with session.post(url=logwebhook, data={"content": msg}) as r:
        if r.status not in [200, 201, 204]:
          print("Failed to log:", r.status)