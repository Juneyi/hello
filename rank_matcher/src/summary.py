def build_summary(target_date, rows, source_files):
    launch_count = len(rows)
    free_ranked_count = sum(1 for r in rows if r["免费榜排名"] != "未上榜")
    paid_ranked_count = sum(1 for r in rows if r["付费榜排名"] != "未上榜")
    both_ranked_count = sum(1 for r in rows if r["免费榜排名"] != "未上榜" and r["付费榜排名"] != "未上榜")
    unranked_count = sum(1 for r in rows if r["免费榜排名"] == "未上榜" and r["付费榜排名"] == "未上榜")
    manual_check_count = sum(1 for r in rows if r["是否需要人工确认"] == "是")
    return {
        "target_date": target_date,
        "launch_count": launch_count,
        "free_ranked_count": free_ranked_count,
        "paid_ranked_count": paid_ranked_count,
        "both_ranked_count": both_ranked_count,
        "unranked_count": unranked_count,
        "manual_check_count": manual_check_count,
        "source_files": source_files,
    }
