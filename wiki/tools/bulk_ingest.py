#!/usr/bin/env python3
"""bulk_ingest.py — Generate skeleton source pages for all remaining albums.

Run from repo root:
    python wiki/tools/bulk_ingest.py         # all missing
    python wiki/tools/bulk_ingest.py --dry-run
    python wiki/tools/bulk_ingest.py --only 专题讲演

Reads catalog.json + doc/影音/ transcripts, writes wiki/<类别>/<相簿>.md
for every album not yet present. Frontmatter and ## 原始资料与影音 table are
accurate; 概要/重点 are auto-extracted stubs to be refined via lint.

Incremental: skips existing wiki pages.
"""

import argparse
import json
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from api_client import build_numbered_asset_url  # noqa: E402

CATALOG = "catalog.json"
WIKI_ROOT = "wiki"
DOC_ROOT = os.path.join("doc", "影音")

def sanitize(name):
    return re.sub(r'[\\/:*?"<>|]+', "_", name).strip()

def read_place_from_doc(album):
    doc_dir = os.path.join(DOC_ROOT, *album["path"], sanitize(album["title"]))
    try:
        files = sorted([f for f in os.listdir(doc_dir) if f.endswith(".md")])
        if not files:
            return ""
        first = open(os.path.join(doc_dir, files[0]), encoding="utf-8").readline().strip()
        parts = [p for p in first.split("　　") if p]
        if len(parts) >= 4:
            cand = parts[3]
            if not cand.startswith("档名"):
                if not re.match(r"^\d{4}[-/]", cand):
                    return cand
    except Exception:
        pass
    return ""

def extract_summary(album):
    doc_dir = os.path.join(DOC_ROOT, *album["path"], sanitize(album["title"]))
    try:
        files = sorted([f for f in os.listdir(doc_dir) if f.endswith(".md")])
        if not files:
            return "（文稿尚未精读，待补概要。）", []
        text = open(os.path.join(doc_dir, files[0]), encoding="utf-8").read()
        lines = [l for l in text.splitlines() if l.strip()]
        if len(lines) >= 2:
            body = "\n".join(lines[1:])
            summary = body.strip()[:400].replace("\n", " ")
            if len(body) > 400:
                summary += "……"
            if not summary:
                summary = "（文稿尚未精读，待补概要。）"
            paras = [p.strip() for p in body.split("\n\n") if p.strip()][:3]
            bullets = []
            for p in paras[:3]:
                snippet = p[:120].replace("\n"," ")
                bullets.append(snippet + ("……" if len(p) > 120 else ""))
            return summary, bullets
    except Exception:
        pass
    return "（文稿尚未精读，待补概要。）", []

def build_page(album, category, topic, dry_run=False):
    title = album["title"]
    pages = len(album["episodes"])
    first = album["episodes"][0] if pages>0 else {}
    code = "-".join((first.get("num") or first.get("video") or first.get("audio") or "").split("-")[:2])
    # date may be timestamp or string
    date_raw = first.get("lecture_time") or ""
    date = str(date_raw)
    if isinstance(date_raw, int) or (isinstance(date_raw, str) and str(date_raw).isdigit()):
        try:
            import time
            ts = int(date_raw)
            if ts > 1000000000:
                date = time.strftime("%Y-%m-%d", time.localtime(ts))
        except Exception:
            pass
    place = read_place_from_doc(album)
    raw = "doc/影音/" + "/".join(album["path"] + [sanitize(title)]) + "/"
    media = ["mp4", "mp3"]  # xiuliuhe always has video+audio via s.liuhejing.cc

    summary, bullets = extract_summary(album)

    tags = [category]
    if topic:
        tags.append(topic)
    if len(tags) > 3:
        tags = tags[:3]

    enc_raw = urllib.parse.quote(raw.rstrip("/"), safe="/")

    rows = []
    for idx, ep in enumerate(sorted(album["episodes"], key=lambda e: e.get("episode") or e.get("num") or "")):
        num = ep.get("num") or ep.get("video") or ep.get("audio") or f"ep{idx+1}"
        ep_file = urllib.parse.quote(f"{raw}{num}.md", safe="/")
        md_link = f"https://github.com/l2yao/xiuliuhe/blob/main/{ep_file}"
        # text link (md only; no doc download for xiuliuhe)
        text_cell = f"[md]({md_link})"
        # media cell - both mp4 and mp3 + hls + poster
        mp4 = build_numbered_asset_url("https://s.liuhejing.cc/", "mp4", num, "mp4")
        mp3 = build_numbered_asset_url("https://s.liuhejing.cc/", "mp3", num, "mp3")
        m3u8 = build_numbered_asset_url("https://s.liuhejing.cc/", "m3u8", num, "m3u8")
        media_parts = [f"[mp4]({mp4})", f"[mp3]({mp3})", f"[m3u8]({m3u8})"]
        media_cell = " · ".join(media_parts)
        rows.append(f"| {idx+1} | {num} | {text_cell} | {media_cell} |")

    topic_line = f"topic: {topic}" if topic else "topic:"
    tags_str = ", ".join(tags)

    frontmatter = f"""---
type: source
category: {category}
{topic_line}
code: {code}
title: {title}
date: {date}
place: {place}
pages: {pages}
raw: {raw}
media: [{", ".join(media)}]
tags: [{tags_str}]
created: 2026-08-27
updated: 2026-08-27
---
"""

    body = f"""# {title}（{code}）

- **档名**：{first.get("num") or "—"}（系列前缀 `{code}`）
- **类别**：{category}{" / " + topic if topic else ""}
- **集数**：共 {pages} 集
- **日期地点**：{date or "—"}，{place or "—"}
- **原始路径**：`{raw}`

## 概要

{summary}

> 注：此为批量生成的初稿概要，待人工精读补充。

## 重点

"""

    if bullets:
        for b in bullets:
            num0 = first.get("num") or ""
            body += f"- {b}〔{num0}〕\n"
    else:
        body += "- （待补）\n"

    body += f"""
## 相关概念

- [[概念/念佛]] [[概念/修六和]]

## 相关页面

- [[{category}]] — 类别页
"""

    body += f"""
## 原始资料与影音

原始资料夹：[GitHub](https://github.com/l2yao/xiuliuhe/tree/main/{enc_raw})（逐集 `md`）

| 集数 | 档名 | 文字 | 影音 |
|---|---|---|---|
"""
    body += "\n".join(rows) + "\n"

    content = frontmatter + "\n" + body

    is_dup = title in DUP_TITLES if 'DUP_TITLES' in globals() else False
    if is_dup:
        if topic:
            out_path = os.path.join(WIKI_ROOT, sanitize(category), sanitize(f"{topic}_{title}") + ".md")
            if os.path.exists(out_path):
                alt = os.path.join(WIKI_ROOT, sanitize(category), sanitize(f"{title}_{album['id']}") + ".md")
                if os.path.exists(alt):
                    return "skip", alt
                out_path = alt
        else:
            out_path = os.path.join(WIKI_ROOT, sanitize(category), sanitize(f"{title}_{album['id']}") + ".md")
            if os.path.exists(out_path):
                return "skip", out_path
    else:
        out_path = os.path.join(WIKI_ROOT, sanitize(category), sanitize(title) + ".md")
        if os.path.exists(out_path):
            return "skip", out_path

    if dry_run:
        return "dry-run", out_path
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    open(out_path, "w", encoding="utf-8").write(content)
    return "created", out_path

def collect_albums(categories):
    albums = []
    def walk(node):
        for a in node.get("albums") or []:
            yield a
        for c in node.get("children") or []:
            yield from walk(c)
    for cat in categories:
        for a in walk(cat):
            yield a

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default=None)
    args = ap.parse_args()

    catalog = json.load(open(CATALOG, encoding="utf-8"))
    cats = catalog["categories"]
    from collections import Counter
    all_titles = [a["title"] for a in collect_albums(cats)]
    global DUP_TITLES
    DUP_TITLES = {t for t, c in Counter(all_titles).items() if c > 1}

    created = skipped = dry = 0
    for album in collect_albums(cats):
        cat = album["path"][0] if album["path"] else "未分类"
        topic = album["path"][1] if len(album["path"]) > 1 else ""
        if args.only and args.only not in cat and args.only not in album["title"] and args.only not in (album.get("album_num") or ""):
            continue
        status, path = build_page(album, cat, topic, dry_run=args.dry_run)
        if status == "created":
            created += 1
            print(f"✓ {cat} / {album['title']} -> {path}")
        elif status == "skip":
            skipped += 1
        elif status == "dry-run":
            dry += 1
    print(f"\nDone. created={created} skipped={skipped} dry={dry}")

if __name__ == "__main__":
    main()
