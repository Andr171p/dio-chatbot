import logging

import hashlib
from pathlib import Path

from typing import List, Optional

from fastapi import UploadFile

from src.misc.files import get_filename, get_file_extension, awrite_bytes
from src.services.upload_file_savers.base_upload_file_saver import BaseUploadFileSaver
from src.services.upload_file_savers.constants import UPLOADED_FILES_DIR, ALLOWED_EXTENSIONS


logger = logging.getLogger(__name__)


class LocalUploadFileSaver(BaseUploadFileSaver):
    def __init__(self, upload_file: UploadFile) -> None:
        self._upload_file = upload_file

    @property
    def _file_extension(self) -> str:
        return get_file_extension(self._upload_file.filename)

    @staticmethod
    def _file_hash(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    @property
    def _file_hashes(self) -> List[str]:
        return [get_filename(file_path.name) for file_path in Path(UPLOADED_FILES_DIR).iterdir()]

    def _is_exists_file_hash(self, file_hash: str) -> bool:
        return file_hash in self._file_hashes

    def _is_allowed_file(self) -> bool:
        return self._file_extension in ALLOWED_EXTENSIONS

    def _file_path(self, file_hash: str) -> str:
        return str(UPLOADED_FILES_DIR / f"{file_hash}.{self._file_extension}")

    async def save(self) -> Optional[str]:
        if not self._is_allowed_file():
            logger.error("File is not supported")
            raise ValueError("File not supported")
        data = await self._upload_file.read()
        file_hash = self._file_hash(data)
        if self._is_exists_file_hash(file_hash):
            logger.warning("File already exists")
            return None
        file_path = self._file_path(file_hash)
        await awrite_bytes(file_path, data)
        logger.debug("File successfully save local")
        return file_path
