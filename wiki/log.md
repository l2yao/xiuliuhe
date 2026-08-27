---
type: log
updated: 2026-08-27
---

# 活动日志

本日志按时间倒序追加，每条以 `## [YYYY-MM-DD] type|detail` 开头，可用 `grep "^## \[" wiki/log.md` 解析。

## [2026-08-27] schema|初始化 xiuliuhe LLM wiki 骨架
搭建 `AGENTS.md`、`wiki/SCHEMA.md`、`wiki/README.md`、`wiki/index.md`、`wiki/tools/*.py` 及 `api_client.py`/`fetch_catalog.py`/`download.py`/`gen_manifest.py`，适配 `m.xiuliuhe.org/api/`。探测到 `https://s.liuhejing.cc/` / `https://d.liuhejing.cc/` 影音 host，验证 `mp4`/`mp3`/`m3u8`/`image` 路径；`catalog.json` 待同步。

## [2026-08-27] sync|catalog 待同步
执行 `python wiki/tools/fetch_catalog.py` 将生成 `catalog.json`（2 类别、约 33 相簿、200+ 集），随后 `download.py` / `gen_manifest.py`。

## [2026-08-27] sync|fetch_catalog → catalog.json 2类别 33相簿 218集
`python wiki/tools/fetch_catalog.py`：`无量寿经` 1/90、`专题讲演` 32/128；过滤 4 条 junk（覺海之舟 `用户协议`等无 num）后总计 218 集。

## [2026-08-27] sync|download 218集 + gen_manifest
`python wiki/tools/download.py` 增量同步完成（已验证 `智海拾零` 首行 `档名：PC-046-0001`）；`python wiki/tools/gen_manifest.py` 生成 `wiki/raw-manifest.md`（33 系列、218 集）。

## [2026-08-27] ingest|bulk 33相簿骨架页
`python wiki/tools/bulk_ingest.py` 批量生成 33 个 source 页（概要/重点为初稿，待精读），写入 `wiki/无量寿经/` 与 `wiki/专题讲演/`；更新 `专题讲演.md`/`无量寿经.md` 类别页。
