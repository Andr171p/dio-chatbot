'''import logging

from src.presentation.api.app import create_fastapi_app


logging.basicConfig(level=logging.INFO)

app = create_fastapi_app()'''


import logging
import asyncio

from src.presentation.bot.main import run_bot


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await run_bot()


if __name__ == "__main__":
    asyncio.run(main())
