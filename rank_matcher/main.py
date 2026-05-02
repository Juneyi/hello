import argparse
from datetime import date
from pathlib import Path

import pandas as pd
import yaml

from src.exporter import export_results
from src.file_finder import FileFinderError, find_latest_file
from src.matcher import build_alias_lookup, build_lookup, match_one
from src.rank_builder import build_rank
from src.reader import ReaderError, read_alias_map, read_launch_file, read_rank_file
from src.summary import build_summary


def resolve_target_date(cli_date, cfg_date):
    if cli_date:
        return cli_date
    if cfg_date:
        return cfg_date
    return date.today().isoformat()


def filter_launch_today(df, target_date):
    dt = pd.to_datetime(df["上架时间"], errors="coerce")
    return df[dt.dt.strftime("%Y-%m-%d") == target_date].copy()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date")
    parser.add_argument("--input-dir")
    parser.add_argument("--launch")
    parser.add_argument("--free")
    parser.add_argument("--paid")
    args = parser.parse_args()

    with open("config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    input_dir = args.input_dir or cfg["input"]["input_dir"]
    target_date = resolve_target_date(args.date, cfg["date"].get("target_date"))

    try:
        launch_file = Path(args.launch) if args.launch else find_latest_file(input_dir, cfg["file_patterns"]["launch_file_keyword"])
        free_file = Path(args.free) if args.free else find_latest_file(input_dir, cfg["file_patterns"]["free_rank_keyword"])
        paid_file = Path(args.paid) if args.paid else find_latest_file(input_dir, cfg["file_patterns"]["paid_rank_keyword"])
    except FileFinderError as e:
        raise SystemExit(str(e))

    if launch_file is None:
        raise SystemExit("未找到漫剧导出文件")
    if free_file is None:
        raise SystemExit("未找到免费榜文件")
    if paid_file is None:
        raise SystemExit("未找到付费榜文件")

    try:
        launch_df = read_launch_file(launch_file)
        free_df = read_rank_file(free_file, "免费")
        paid_df = read_rank_file(paid_file, "付费")
        alias_df = read_alias_map(cfg["input"]["alias_map_file"])
    except ReaderError as e:
        raise SystemExit(str(e))

    today_df = filter_launch_today(launch_df, target_date)
    free_rank_df, free_dup_id, free_dup_name = build_rank(free_df, "免费榜排名")
    paid_rank_df, paid_dup_id, paid_dup_name = build_rank(paid_df, "付费榜排名")

    free_by_id, free_by_name = build_lookup(free_rank_df, "免费榜排名")
    paid_by_id, paid_by_name = build_lookup(paid_rank_df, "付费榜排名")
    alias_lookup = build_alias_lookup(alias_df)
    fuzzy_threshold = int(cfg["matching"]["fuzzy_threshold"])

    rows = []
    for _, row in today_df.iterrows():
        did = str(row.get("短剧ID", "")).strip()
        dname = str(row.get("短剧名称", "")).strip()

        free_match = match_one(did, dname, free_by_id, free_by_name, alias_lookup, fuzzy_threshold)
        paid_match = match_one(did, dname, paid_by_id, paid_by_name, alias_lookup, fuzzy_threshold)

        anomalies = []
        if free_match.rank is None:
            anomalies.append("免费榜未上榜")
        if paid_match.rank is None:
            anomalies.append("付费榜未上榜")
        if free_match.need_manual_check:
            anomalies.append("免费榜匹配置信度较低，需人工确认")
        if paid_match.need_manual_check:
            anomalies.append("付费榜匹配置信度较低，需人工确认")
        if free_dup_id:
            anomalies.append("免费榜存在重复剧ID，需人工确认")
        if free_dup_name:
            anomalies.append("免费榜存在重复剧名，需人工确认")
        if paid_dup_id:
            anomalies.append("付费榜存在重复剧ID，需人工确认")
        if paid_dup_name:
            anomalies.append("付费榜存在重复剧名，需人工确认")

        rows.append({
            "目标日期": target_date,
            "短剧ID": did,
            "短剧名称": dname,
            "上架时间": row.get("上架时间", ""),
            "男/女频": row.get("男/女频", ""),
            "版权方": row.get("版权方", ""),
            "总集数": row.get("总集数", ""),
            "免费榜排名": free_match.rank if free_match.rank is not None else "未上榜",
            "付费榜排名": paid_match.rank if paid_match.rank is not None else "未上榜",
            "免费榜匹配方式": free_match.method,
            "付费榜匹配方式": paid_match.method,
            "免费榜匹配置信度": free_match.confidence,
            "付费榜匹配置信度": paid_match.confidence,
            "是否需要人工确认": "是" if (free_match.need_manual_check or paid_match.need_manual_check) else "否",
            "异常说明": "；".join(anomalies) if anomalies else "正常",
        })

    if len(rows) == 0:
        rows = []

    summary = build_summary(target_date, rows, {
        "launch_file": launch_file.name,
        "free_rank_file": free_file.name,
        "paid_rank_file": paid_file.name,
    })

    export_results(rows, cfg["output"]["excel_file"], cfg["output"]["json_file"], summary)
    print("完成：", cfg["output"]["excel_file"], cfg["output"]["json_file"])


if __name__ == "__main__":
    main()
