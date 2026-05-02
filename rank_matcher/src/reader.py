from pathlib import Path
import pandas as pd

LAUNCH_REQUIRED = ["短剧ID", "短剧名称", "上架时间"]
RANK_REQUIRED = ["剧ID", "剧名"]


class ReaderError(Exception):
    pass


def _read_any(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    return pd.read_excel(path)


def read_launch_file(path: Path) -> pd.DataFrame:
    df = _read_any(path)
    missing = [c for c in LAUNCH_REQUIRED if c not in df.columns]
    if missing:
        raise ReaderError(f"漫剧导出文件缺少必要字段: {','.join(missing)}")
    return df


def read_rank_file(path: Path, rank_type: str) -> pd.DataFrame:
    df = _read_any(path)
    missing = [c for c in RANK_REQUIRED if c not in df.columns]
    if missing:
        raise ReaderError(f"{rank_type}榜文件缺少必要字段: {','.join(missing)}")
    return df


def read_alias_map(path: str):
    p = Path(path)
    if not p.exists():
        return None
    df = pd.read_csv(p)
    for col in ["短剧ID", "标准剧名", "别名"]:
        if col not in df.columns:
            raise ReaderError(f"alias_map.csv 缺少字段: {col}")
    return df
