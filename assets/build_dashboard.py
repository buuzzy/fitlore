#!/usr/bin/env python3
"""fitlore 可视化构建脚本。

用法：
    python3 build_dashboard.py --data data.json --out dashboard.html

输入 data.json 结构（字段均可留空数组，缺数据的板块会自动隐藏）：
{
  "user": "用户名",
  "title": "2026-10 月度复盘 · 数据可视化",
  "period": "2026-08-01 ~ 2026-10-17",
  "generated_at": "2026-10-18",
  "notes": ["备注一", "备注二"],
  "measurements": [
    {"date": "2026-08-02", "weight_kg": 79.8, "bodyfat_pct": null,
     "sleep_h": null, "sleep_score": null}
  ],
  "weeks": [
    {"week": "W32", "sessions": 3, "volume_kg": 18200, "duration_min": 190}
  ],
  "exercises": [
    {"name": "卧推", "unit": "kg",
     "points": [{"date": "2026-08-03", "weight": 60, "reps": 8}]}
  ]
}

输出：自包含 HTML（ECharts 已内嵌，双击即可在浏览器打开，无需服务器）。
"""
import argparse
import json
import sys
from pathlib import Path

ASSET_DIR = Path(__file__).resolve().parent
PLACEHOLDER_JS = "__ECHARTS_JS__"
PLACEHOLDER_DATA = "__DATA_JSON__"


def build(data_path: Path, out_path: Path) -> None:
    template_path = ASSET_DIR / "dashboard-template.html"
    echarts_path = ASSET_DIR / "echarts.min.js"
    for p in (template_path, echarts_path, data_path):
        if not p.exists():
            sys.exit(f"错误：找不到文件 {p}")

    raw = data_path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(f"错误：{data_path} 不是合法 JSON：{e}")

    # 基本结构兜底：缺字段补空值，保证模板渲染不报错
    data.setdefault("user", "")
    data.setdefault("title", "健身数据报告")
    data.setdefault("period", "")
    data.setdefault("generated_at", "")
    data.setdefault("notes", [])
    data.setdefault("measurements", [])
    data.setdefault("weeks", [])
    data.setdefault("exercises", [])

    template = template_path.read_text(encoding="utf-8")
    echarts_js = echarts_path.read_text(encoding="utf-8")

    if PLACEHOLDER_JS not in template or PLACEHOLDER_DATA not in template:
        sys.exit("错误：模板缺少占位符，请检查 dashboard-template.html")

    html = template.replace(PLACEHOLDER_JS, echarts_js)
    html = html.replace(
        PLACEHOLDER_DATA,
        json.dumps(data, ensure_ascii=False),
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    # 简单自检
    ok_js = PLACEHOLDER_JS not in html
    ok_data = PLACEHOLDER_DATA not in html
    size_kb = out_path.stat().st_size / 1024
    print(f"已生成：{out_path}（{size_kb:.0f} KB）")
    print(f"自检：ECharts 注入 {'通过' if ok_js else '失败'}，数据注入 {'通过' if ok_data else '失败'}")
    if not (ok_js and ok_data):
        sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser(description="生成自包含的健身数据可视化 HTML")
    ap.add_argument("--data", required=True, help="数据 JSON 文件路径")
    ap.add_argument("--out", required=True, help="输出 HTML 路径")
    args = ap.parse_args()
    build(Path(args.data), Path(args.out))


if __name__ == "__main__":
    main()
