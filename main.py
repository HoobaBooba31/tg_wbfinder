from client import bot
import asyncio
import uvicorn
from api import api

async def main():
    await asyncio.gather(server.serve(), bot.start_bot())

if __name__ == '__main__':
    config = uvicorn.Config(api.app, host="0.0.0.0", port=8000, loop="asyncio", reload=False)
    server = uvicorn.Server(config)

    asyncio.run(main())
