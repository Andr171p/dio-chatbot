from typing import Union

from pathlib import Path


def read_txt(file_path: Union[Path, str]) -> str:
    with open(file_path, encoding="utf-8") as file:
        return file.read()
