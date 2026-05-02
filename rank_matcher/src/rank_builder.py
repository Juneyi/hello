import pandas as pd


def build_rank(df: pd.DataFrame, rank_name: str):
    out = []
    rank = 0
    duplicate_id = False
    duplicate_name = False

    ids = df["剧ID"].fillna("").astype(str).str.strip()
    names = df["剧名"].fillna("").astype(str).str.strip()

    valid = ~((ids == "") & (names == ""))
    seen_id = set()
    seen_name = set()

    for _, row in df[valid].iterrows():
        drama_id = str(row.get("剧ID", "")).strip()
        drama_name = str(row.get("剧名", "")).strip()
        rank += 1
        out.append({"剧ID": drama_id, "剧名": drama_name, rank_name: rank})

        if drama_id:
            if drama_id in seen_id:
                duplicate_id = True
            seen_id.add(drama_id)
        if drama_name:
            if drama_name in seen_name:
                duplicate_name = True
            seen_name.add(drama_name)

    return pd.DataFrame(out), duplicate_id, duplicate_name
