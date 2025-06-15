from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Optional

try:
    import win32api  # type: ignore
    import win32con  # type: ignore
    import win32file  # type: ignore
except ImportError:  # pragma: no cover
    win32api = None  # type: ignore

logger = logging.getLogger(__name__)


def file_hash(path: str | Path, block_size: int = 65536) -> str:
    """Calcula SHA-256 de un archivo. Devuelve string vacío si falla."""

    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:  # noqa: PTH123
            for chunk in iter(lambda: f.read(block_size), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception as exc:  # pragma: no cover
        logger.debug("No se pudo calcular hash", path=str(path), exc_info=exc)
        return ""


def is_file_signed(path: str | Path) -> bool:
    """Comprueba si el binario tiene firma digital válida (WinVerifyTrust).
    Si pywin32 no está disponible o error → False.
    """

    if win32api is None:  # pragma: no cover
        return False

    try:
        from win32com.client import Dispatch  # type: ignore

        signer = Dispatch("CAPICOM.Signer")  # noqa: S608
        signed_data = Dispatch("CAPICOM.SignedCode")  # noqa: S608
        signed_data.FileName = str(path)
        signed_data.Verify()  # Lanza excepción si no es válido
        return True
    except Exception:  # pragma: no cover
        return False 