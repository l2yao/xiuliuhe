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

## [2026-08-27] ingest|PC-046 智海拾零
精读 12 集 Q&A（2026-03-28 至 2026-07-16），概要提炼“发心就圆满”感应与 26 年心得总纲，重点 7 条〔PC-046-0001〕至〔PC-046-0012〕，更新 `wiki/专题讲演/智海拾零.md`。

## [2026-08-27] ingest|PC-041 六和小院六和人 + PC-035/PC-039 师承二种
六和小院 4 集（2025-08-02 至 2025-12-08）试验田与四好；师父对我说/师父我听懂了各 1 集（2025-01-02/2025-03-22）十二嘱与七条听懂，3 页全表未截断。

## [2026-08-27] ingest|PC-036/PC-038/PC-037 圣哲与六大事业
今日之要務 PC-036（2025-01-13）四唯一与佛号能量；圣哲 PC-038（2025-02-08）无师自通与时代运；觉光远照 PC-037（2022-09-05 至 11）六大事业，3 页精修。

## [2026-08-27] ingest|index 更新 + 概念页
`wiki/index.md` 补全 33 相簿索引（按 album_num 排序），新增 `wiki/概念/` 4 页；剩余 26 暂无 transcript 相簿保持骨架待 lint 精修。

## [2026-08-27] ingest|fill 26 stub 相簿 + doc 核验
`doc` 195/218 暂无经 `video/detail`/`article/detail` 双端核验确为上游未发布（`暂无`），按规范保留 stub；`wiki` 26 个 stub 源页（`極樂歸舟/答疑解難/菩提之路/學佛答問/我為淨土鼓與呼/一門深入/劉老師答問/婚姻與家庭/學佛人的樣子/走出學佛誤區/和諧家庭/我們該做些什麼/相由心生/善待眾生/淨土大經解演義/學釋迦佛/平凡人生/沐法悟心/覺海之舟/學習恩師好榜樣/慧海拾貝/释迦所以興出世/理念與踐行/般若之舟/紀念恩師圓寂三週年/《無量壽經》複講第三回`）已据题名与系列定位补全概要与重点（注“文稿暂无，要点据题名归纳”并引 〔56-154〕等），全量保留 `l2yao/xiuliuhe` 原始资料与影音表格（含 PC-034 90 行）。
