from pathlib import Path
from typing import Optional

SUPPORTED_EXTS = {".xlsx", ".xls", ".csv"}


class FileFinderError(Exception):
    pass


def find_latest_file(input_dir: str, keyword: str) -> Optional[Path]:
    base = Path(input_dir)
    if not base.exists():
        raise FileFinderError(f"输入目录不存在: {input_dir}")
    if not base.is_dir():
        raise FileFinderError(f"输入路径不是目录: {input_dir}")

    candidates = [
        p for p in base.iterdir()
        if p.is_file() and keyword in p.name and p.suffix.lower() in SUPPORTED_EXTS
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)
