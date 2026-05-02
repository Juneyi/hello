from pathlib import Path
import time

from src.file_finder import find_latest_file


def test_find_latest_files(tmp_path: Path):
    f1 = tmp_path / "漫剧导出_a.xlsx"
    f1.write_text("x")
    time.sleep(0.01)
    f2 = tmp_path / "漫剧导出_b.csv"
    f2.write_text("x")
    assert find_latest_file(str(tmp_path), "漫剧导出") == f2
