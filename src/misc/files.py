import aiofiles
from typing import Union
from pathlib import Path


def get_filename(file_path: str) -> str:
    return file_path.split(".")[-2]


def get_file_extension(file_path: str) -> str:
    return file_path.split(".")[-1]


def write_bytes(file_path: Union[Path, str], data: bytes) -> None:
    with open(file_path, mode="wb") as file:
        file.write(data)


async def awrite_bytes(file_path: Union[Path, str], data: bytes) -> None:
    async with aiofiles.open(file_path, mode="wb") as file:
        await file.write(data)


def read_txt(file_path: Union[Path, str]) -> str:
    with open(file_path, encoding="utf-8") as file:
        return file.read()


async def aread_txt(file_path: Union[Path, str]) -> str:
    async with open(file_path, encoding="utf-8") as file:
        return await file.read()
