import pandas as pd

from src.rank_builder import build_rank


def test_rank_build_and_skip_empty():
    df = pd.DataFrame({"剧ID": ["1", "", "2"], "剧名": ["A", "", "B"]})
    out, dup_id, dup_name = build_rank(df, "免费榜排名")
    assert list(out["免费榜排名"]) == [1, 2]
    assert not dup_id
    assert not dup_name
