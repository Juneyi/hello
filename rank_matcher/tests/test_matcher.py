import pandas as pd

from src.matcher import build_alias_lookup, build_lookup, match_one


def test_id_exact_title_alias_fuzzy():
    rank_df = pd.DataFrame([
        {"剧ID": "100", "剧名": "总裁的替嫁新娘", "免费榜排名": 1},
        {"剧ID": "200", "剧名": "霸道总裁爱上我", "免费榜排名": 2},
    ])
    by_id, by_name = build_lookup(rank_df, "免费榜排名")
    alias_df = pd.DataFrame([{"短剧ID": "100", "标准剧名": "总裁的替嫁新娘", "别名": "替嫁新娘"}])
    alias = build_alias_lookup(alias_df)

    assert match_one("100", "x", by_id, by_name, alias, 90).method == "id_exact"
    assert match_one("", "总裁的替嫁新娘", by_id, by_name, alias, 90).method == "title_exact"
    assert match_one("", "替嫁新娘", by_id, by_name, alias, 90).method == "alias_map"
    low = match_one("", "完全不一样", by_id, by_name, alias, 95)
    assert low.method == "fuzzy"
    assert low.need_manual_check
