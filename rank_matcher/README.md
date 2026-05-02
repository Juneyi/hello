# rank_matcher

本地 MVP 工具：识别今日上线新剧，并匹配其在免费榜/付费榜的小时排名。

## 1. 项目用途
- 扫描 `data/input/` 自动识别最新输入文件
- 筛选目标日期上架新剧
- 生成免费榜/付费榜排名并匹配
- 输出 Excel + JSON

## 2. 文件命名规则
- 漫剧导出：文件名包含 `漫剧导出`
- 免费榜：文件名包含 `免费漫剧`
- 付费榜：文件名包含 `付费漫剧`
- 支持 `.xlsx/.xls/.csv`，同类多个取最新修改时间

## 3. 字段要求
- 漫剧导出必需：`短剧ID` `短剧名称` `上架时间`
- 榜单必需：`剧ID` `剧名`
- alias_map 可选：`短剧ID` `标准剧名` `别名`

## 4. 配置
见 `config.yaml`：输入目录、文件关键词、输出路径、模糊阈值、默认日期。

## 5. 运行
```bash
python main.py
python main.py --date 2026-05-02
python main.py --input-dir data/input --date 2026-05-02
python main.py --launch "...xlsx" --free "...xlsx" --paid "...xlsx" --date 2026-05-02
```

## 6. 匹配逻辑
1) ID 精确匹配
2) 标准化剧名精确匹配
3) alias_map 别名匹配
4) rapidfuzz 模糊匹配（低于阈值标记人工确认）

## 7. 榜单排名规则
按有效数据行顺序从 1 开始；空行与 ID/剧名都为空的行不计入。

## 8. 输出说明
- Excel: `data/output/rank_match_result.xlsx`
- JSON: `data/output/rank_match_result.json`
包含 summary 与 items，便于后续分析。

## 9. 常见错误
- 输入目录不存在
- 找不到某类文件
- 缺少必要字段
