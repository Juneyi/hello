import json
from pathlib import Path
import pandas as pd


def export_results(rows, excel_path: str, json_path: str, summary: dict):
    excel_p = Path(excel_path)
    json_p = Path(json_path)
    excel_p.parent.mkdir(parents=True, exist_ok=True)
    json_p.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(rows).to_excel(excel_p, index=False)

    items = []
    for r in rows:
        items.append({
            "target_date": r["目标日期"],
            "drama_id": r["短剧ID"],
            "drama_name": r["短剧名称"],
            "launch_time": str(r["上架时间"]),
            "gender_channel": r.get("男/女频", ""),
            "copyright_owner": r.get("版权方", ""),
            "total_episodes": r.get("总集数", ""),
            "free_rank": r["免费榜排名"],
            "paid_rank": r["付费榜排名"],
            "free_match_method": r["免费榜匹配方式"],
            "paid_match_method": r["付费榜匹配方式"],
            "free_confidence": r["免费榜匹配置信度"],
            "paid_confidence": r["付费榜匹配置信度"],
            "need_manual_check": r["是否需要人工确认"] == "是",
            "anomaly_reason": r["异常说明"],
        })

    with open(json_p, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "items": items}, f, ensure_ascii=False, indent=2)
