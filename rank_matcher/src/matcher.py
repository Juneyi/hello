from dataclasses import dataclass
from typing import Dict, Optional

from rapidfuzz import fuzz

from .normalizer import normalize_title


@dataclass
class MatchResult:
    rank: Optional[int]
    method: str
    confidence: int
    need_manual_check: bool


def build_lookup(rank_df, rank_col: str):
    by_id = {}
    by_name = {}
    for _, row in rank_df.iterrows():
        drama_id = str(row.get("剧ID", "")).strip()
        drama_name = str(row.get("剧名", "")).strip()
        norm = normalize_title(drama_name)
        if drama_id and drama_id not in by_id:
            by_id[drama_id] = int(row[rank_col])
        if norm and norm not in by_name:
            by_name[norm] = int(row[rank_col])
    return by_id, by_name


def build_alias_lookup(alias_df):
    alias_to_id = {}
    if alias_df is None:
        return alias_to_id
    for _, row in alias_df.iterrows():
        aid = str(row.get("短剧ID", "")).strip()
        alias = normalize_title(str(row.get("别名", "")).strip())
        if aid and alias:
            alias_to_id[alias] = aid
    return alias_to_id


def match_one(drama_id: str, drama_name: str, by_id: Dict[str, int], by_name: Dict[str, int],
              alias_to_id: Dict[str, str], fuzzy_threshold: int) -> MatchResult:
    did = str(drama_id).strip()
    norm_name = normalize_title(drama_name)

    if did and did in by_id:
        return MatchResult(by_id[did], "id_exact", 100, False)
    if norm_name and norm_name in by_name:
        return MatchResult(by_name[norm_name], "title_exact", 100, False)
    if norm_name and norm_name in alias_to_id:
        alias_id = alias_to_id[norm_name]
        if alias_id in by_id:
            return MatchResult(by_id[alias_id], "alias_map", 100, False)

    best_name = None
    best_score = -1
    for candidate in by_name.keys():
        score = fuzz.ratio(norm_name, candidate)
        if score > best_score:
            best_score = score
            best_name = candidate
    if best_name is None:
        return MatchResult(None, "unmatched", 0, False)

    rank = by_name[best_name]
    need_manual = best_score < fuzzy_threshold
    return MatchResult(rank, "fuzzy", int(best_score), need_manual)
