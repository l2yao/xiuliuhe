#!/usr/bin/env python3
"""download.py — Download episode transcripts from the xiuliuhe API into doc/影音/….

Run from the xiuliuhe repo root:
    python wiki/tools/download.py                    # all episodes (incremental)
    python wiki/tools/download.py --only PC-046      # only albums whose code prefix matches
    python wiki/tools/download.py --dry-run

Input: catalog.json (produced by fetch_catalog.py).
Output: doc/影音/<类别>/<相簿>/<NUM>.md
    Each page first line is metadata:
        题目　　（共N集｜第N集）　　日期　　档名：NUM
    followed by the transcript rendered as clean markdown.

Incremental: episodes already on disk (by num) are skipped.

No external dependencies (uses only the stdlib + wiki/tools/api_client.py).
"""

import argparse
import html
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from api_client import video_detail  # noqa: E402

CONCURRENCY = 4
OUT_ROOT = "doc/影音"


# ---------- small HTML -> markdown ----------
def decode_entities(s):
    return html.unescape(s).replace("\xa0", " ")


def html_to_markdown(html_text):
    if not html_text:
        return ""
    text = str(html_text)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</(?:p|div|h\d|li|tr)>", "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</(?:td|th)>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = decode_entities(text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ---------- path helpers ----------
def sanitize(name):
    cleaned = re.sub(r'[\\/:*?"<>|]+', "_", name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def episode_dir(album):
    path = [sanitize(x) for x in (album.get("path") or []) if x]
    return os.path.join(OUT_ROOT, *path, sanitize(album.get("title", "")))


def normalize_date(v):
    # lecture_time may be timestamp int or date string
    if v is None or v == "":
        return ""
    if isinstance(v, int) or (isinstance(v, str) and v.isdigit()):
        try:
            import time
            ts = int(v)
            # xiuliuhe uses seconds (check magnitude)
            if ts > 1000000000 and ts < 3000000000:
                return time.strftime("%Y-%m-%d", time.localtime(ts))
        except Exception:
            pass
    return str(v)


def build_page(episode, album, album_index, album_total):
    num = episode.get("num") or episode.get("video") or episode.get("audio") or ""
    title = episode.get("title", "")
    date = normalize_date(episode.get("lecture_time", "") or "")
    meta = "{}　　（共{}集｜第{}集）　　{}　　档名：{}".format(
        title, album_total, album_index + 1, date, num
    )
    body = html_to_markdown(episode.get("__content") or "")
    if not body:
        body = "<p>暂无</p>"  # keep as markdown placeholder so we know it was stub
        # but html_to_markdown would strip tags -> leave "暂无"
        body = "暂无"
    return "{}\n\n{}\n".format(meta, body)


# ---------- counters ----------
FETCHED = 0
SKIPPED = 0
FAILED = 0
NO_CONTENT = 0


def process_episode(episode, album, album_index, album_total, dry_run):
    global FETCHED, SKIPPED, FAILED, NO_CONTENT
    num = episode.get("num") or episode.get("video") or episode.get("audio") or ""
    dir_path = episode_dir(album)
    file_path = os.path.join(dir_path, "{}.md".format(num)) if num else None
    if not file_path:
        FAILED += 1
        return {"status": "error", "num": num}

    if os.path.exists(file_path):
        SKIPPED += 1
        return {"status": "skip", "num": num}

    if dry_run:
        FETCHED += 1
        return {"status": "dry-run", "num": num}

    try:
        res = video_detail(episode["id"])
        content = (res.get("data") or {}).get("content")
        content = content or ""
        if not content.strip() or content.strip().lower() == "null" or "<p>暂无</p>" in content:
            if "<p>暂无</p>" in content:
                NO_CONTENT += 1
            elif not content.strip():
                NO_CONTENT += 1
            content = content
        episode["__content"] = content
        FETCHED += 1
        page = build_page(episode, album, album_index, album_total)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(page)
        return {"status": "written", "num": num}
    except Exception as err:
        FAILED += 1
        print("  !! {}: {}".format(num, err))
        return {"status": "error", "num": num}


def process_album(album, dry_run):
    episodes = album.get("episodes") or []
    if not episodes:
        return
    first = episodes[0]
    code_prefix = "-".join(
        (first.get("num") or first.get("video") or first.get("audio") or "").split("-")[:2]
    )
    sys.stdout.write(
        "  {} {:>4} eps  {}\n".format(
            code_prefix.ljust(10), len(episodes), album.get("title", "")
        )
    )
    sys.stdout.flush()

    jobs = []
    with ThreadPoolExecutor(max_workers=min(CONCURRENCY, len(episodes) or 1)) as pool:
        for i, ep in enumerate(sorted(episodes, key=lambda e: e.get("episode") or 0)):
            jobs.append(pool.submit(process_episode, ep, album, i, len(episodes), dry_run))
        for fut in as_completed(jobs):
            fut.result()


def collect_albums(categories):
    albums = []

    def walk(node):
        albums.extend(node.get("albums") or [])
        for c in node.get("children") or []:
            walk(c)

    for cat in categories:
        walk(cat)
    return albums


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None, help="only process albums whose code prefix / title / id matches")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with open("catalog.json", encoding="utf-8") as f:
        catalog = json.load(f)

    albums = collect_albums(catalog["categories"])

    if args.only:
        filtered = []
        for a in albums:
            first = (a.get("episodes") or [{}])[0]
            code_prefix = first.get("num") or first.get("video") or first.get("audio") or ""
            if (
                code_prefix.startswith(args.only)
                or args.only in a.get("title", "")
                or args.only in (a.get("album_num") or "")
                or str(a.get("id")) == args.only
            ):
                filtered.append(a)
        albums = filtered

    msg = " DRY RUN, no files written" if args.dry_run else ""
    print("Albums: {} (of {}){}".format(len(albums), len(collect_albums(catalog["categories"])), msg))
    for a in albums:
        process_album(a, args.dry_run)

    print("\nDone.")
    print("  fetched/attempted: {}".format(FETCHED))
    print("  skipped (already on disk): {}".format(SKIPPED))
    print("  failed: {}".format(FAILED))
    print("  no transcript content: {}".format(NO_CONTENT))


if __name__ == "__main__":
    main()
