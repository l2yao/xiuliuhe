# SCHEMA.md — 页面模板与示例（xiuliuhe）

This file documents the exact page templates and examples for the xiuliuhe wiki. Reference `AGENTS.md` for the overall schema. All page content is Simplified Chinese (Traditional titles tolerated). The corpus is 刘素云老师（修六和 / 慈云法语 / m.xiuliuhe.org）的开示.

## 页面类型速览

| 类型 | 位置 | frontmatter `type` |
|---|---|---|
| 类别页 | `wiki/<类别>.md` | `category` |
| 主题页 | `wiki/<类别>/<主题>.md` | `topic` |
| 开示页 | `wiki/<类别>/<相簿标题>.md` | `source` |
| 概念页 | `wiki/概念/<概念>.md` | `concept` |
| 问答页 | `wiki/问答/<题目>.md` | `answer` |

## 模板

### 类别页 (category)

```markdown
---
type: category
category: 专题讲演
tags: [净土, 修六和]
albums: 32
updated: 2026-08-27
---

# 专题讲演

此类别涵盖刘素云老师对念佛与修六和的专题开示：…（一段综合说明）。

## 开示一览

- [[智海拾零]] — …
- [[极乐归舟]] — …

依 [[index|索引]] 与 [[raw-manifest|原始清单]] 查阅。
```

### 主题页 (topic)

```markdown
---
type: topic
category: 无量寿经
title: 修六和
tags: [六和, 净土]
updated: 2026-08-27
---

# 修六和

子分类主题。六和敬要义：…

## 开示

- [[智海拾零]] — …
- …（该子分类下的相簿）

## 相关概念

- [[概念/修六和]] [[概念/菩提心]]
```

### 开示页 (source) — 每个相簿（系列）一页

```markdown
---
type: source
category: 专题讲演
topic:            # 子分类或主题，无则留白
code: PC-046             # num 的首两段，如 PC-034
title: 智海拾零
date: 2026-03-28
place:
pages: 12
raw: doc/影音/专题讲演/智海拾零/
media: [mp4, mp3]
tags: [修心, 念佛]
created: 2026-08-27
updated: 2026-08-27
---

# 智海拾零（PC-046）

- **档名**：PC-046-0001（系列前缀 `PC-046`）
- **类别**：专题讲演
- **集数**：共 12 集
- **日期**：2026-03-28
- **原始路径**：`doc/影音/专题讲演/智海拾零/`

## 概要

一段话说明本开示讲什么。

## 重点

- 要点一〔PC-046-0001〕
- 要点二

## 相关概念

- [[概念/修心]] [[概念/念佛]]

## 相关页面

- [[专题讲演]] — 类别页
- [[极乐归舟]] — 同类别其他开示

## 原始资料与影音

原始资料夹：[GitHub](https://github.com/<owner>/xiuliuhe/tree/main/doc/影音/专题讲演/智海拾零)（逐集 `md`）

| 集数 | 档名 | 文字 | 影音 |
|---|---|---|---|
| 1 | PC-046-0001 | [md](https://github.com/<owner>/xiuliuhe/blob/main/doc/影音/专题讲演/智海拾零/PC-046-0001.md) | [mp4](https://s.liuhejing.cc/mp4/PC/PC-046/PC-046-0001.mp4) · [mp3](https://s.liuhejing.cc/mp3/PC/PC-046/PC-046-0001.mp3) · [m3u8](https://s.liuhejing.cc/m3u8/PC/PC-046/PC-046-0001/PC-046-0001.m3u8) |

> 每集皆须列入；集数多时亦须全列，不得省略。文字与影音链接依该集 `media` frontmatter 取用，永不臆测。URL 一律经 `wiki/tools/api_client.py` 的 `get_video_mp4_url` / `get_audio_mp3_url` / `get_video_hls_url` / `get_poster_url` 产生，不得手拼。
```

### 概念页 (concept)

```markdown
---
type: concept
title: 念佛
tags: [净土]
sources: [PC-034, PC-046]
updated: 2026-08-27
---

# 念佛

定义：…

## 各开示的讲法

- [[智海拾零]] — 强调 …
- [[《無量壽經》複講第三回]] — …

## 要点

- …

## 相关概念

- [[概念/因果]] [[概念/修六和]]

## 引用出处

- 〔PC-034〕〔PC-046〕
```

### 问答页 (answer)

```markdown
---
type: answer
title: 如何对治疑心
tags: [比较, 修持]
updated: 2026-08-27
---

# 标题

**问题**：…

**回答**：…

## 出处

- 〔PC-046-0001〕
- [[智海拾零]]

## 相关页面

- …
```

## 命名与链接规则

- 档名：类别/主题/概念/相簿用中文名（如 `智海拾零.md`）；`NUM` 代码只用于 `doc/` 之下。档名不含空格。
- 内部链接：`[[页面名]]`；开示页链接相簿标题 `[[智海拾零]]`；概念页用 `[[概念/念佛]]`。
- 引用：`〔PC-034〕` 引用整个系列，`〔PC-046-0001〕` 引用特定一集（系列前缀 = `num` 首两段）。
- 开示页需附 `## 原始资料与影音` 区段：原始资料夹的 GitHub 链接（`https://github.com/<owner>/xiuliuhe/tree/main/doc/影音/<路径>`）、每集 `md` 的 GitHub blob（`https://github.com/<owner>/xiuliuhe/blob/main/doc/影音/<路径>/<NUM>.md`），以及官方影音链接（经 `get_video_mp4_url` 等产生）。中文路径在 URL 中须以 UTF-8 百分比编码。
- 影音 URL 格式（host 为 `https://s.liuhejing.cc/`，`NUM` 拆成 `major`/`minor`=前两段）：
  - mp4：`https://s.liuhejing.cc/mp4/{major}/{major}-{minor}/{NUM}.mp4`
  - mp3：`https://s.liuhejing.cc/mp3/{major}/{major}-{minor}/{NUM}.mp3`
  - m3u8（HLS）：`https://s.liuhejing.cc/m3u8/{major}/{major}-{minor}/{NUM}/{NUM}.m3u8`
  - 海报：`https://s.liuhejing.cc/image/{major}/{major}-{minor}/{NUM}.jpg`
  - 备用 host：`https://d.liuhejing.cc/` 同路径（`get_xxx_url(..., host=MEDIA_HOSTS["backup"])`）

## 前导资料 (frontmatter)

可用字段：

| 字段 | 说明 | 例 |
|---|---|---|
| `type` | 页面类型 | `source` |
| `category` | 类别（中文） | `专题讲演` |
| `topic` | 子分类/主题（中文） | `修六和` |
| `code` | 系列前缀（`num` 首两段） | `PC-046` |
| `title` | 开示题目 | `智海拾零` |
| `date` | 开示日期，`YYYY-MM-DD` | `2026-03-28` |
| `place` | 地点（第一集 metaLine 有则填） | `` |
| `pages` | 集数 | `12` |
| `raw` | 原始资料夹路径 | `doc/影音/专题讲演/智海拾零/` |
| `media` | 可取得的链接类型 | `[mp4, mp3]` |
| `tags` | 标签 | `[修心, 念佛]` |
| `created` / `updated` | 日期 | `2026-08-27` |
| `sources` | 概念页引用的系列代码 | `[PC-034, PC-046]` |

## 长度规则

- 单页约 150 行内；超过则拆分。
- 例外：`## 原始资料与影音` 的逐集表格依集数增长，属设计使然，不受行数限制（全表不得截断）。
- 概念页、问答页随内容演化而更新，不需每次重写。
