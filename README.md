# xiuliuhe

LLM Wiki for **修六和 / 慈云法语 / m.xiuliuhe.org**（刘素云老师主讲）. A Python-based, reproducible clone of the xiuliuhe teachings plus an LLM-maintained wiki (Karpathy "LLM Wiki" pattern, same as `xwcz` / `amtb`).

- **Raw corpus** — `doc/影音/` (one markdown per episode), synced from the public API; read-only except via sync tools.
- **Wiki** — `wiki/` (LLM-authored interlinked markdown: categories, topics, albums, concepts, Q&A).
- **Schema** — `AGENTS.md` + `wiki/SCHEMA.md` define structure and workflows.
- **Tools** — `wiki/tools/` (Python): `fetch_catalog.py`, `download.py`, `gen_manifest.py`, `api_client.py`.

## Existing API

Base URL:

```text
https://m.xiuliuhe.org/api/
```

Media hosts:

```text
https://s.liuhejing.cc/  (primary)
https://d.liuhejing.cc/  (backup)
```

URL pattern (via `api_client.py:m(host, code, ext)`):

```text
https://s.liuhejing.cc/mp4/{major}/{major}-{minor}/{NUM}.mp4
https://s.liuhejing.cc/mp3/{major}/{major}-{minor}/{NUM}.mp3
https://s.liuhejing.cc/m3u8/{major}/{major}-{minor}/{NUM}/{NUM}.m3u8
https://s.liuhejing.cc/image/{major}/{major}-{minor}/{NUM}.jpg
```

where `NUM` = `PC-034-0001`, `major`/`minor` = first two segments (`PC`/`034`).

## Sync the raw corpus (LLM wiki)

The API is walked and transcripts downloaded into `doc/影音/` by Python tools in `wiki/tools/` (they share `wiki/tools/api_client.py`). Run from the repo root:

```
python wiki/tools/fetch_catalog.py   # walk categories→albums→episodes → catalog.json
python wiki/tools/download.py        # fetch missing transcripts into doc/影音/… (incremental)
python wiki/tools/gen_manifest.py    # regenerate wiki/raw-manifest.md
```

Use `--only <prefix>` to target one series (e.g. `python wiki/tools/download.py --only PC-046`) or `--dry-run` to preview. Never hand-edit anything under `doc/`.

## Wiki workflows

See `AGENTS.md` for the full schema. Typical flows:

- **Ingest** — pick an album from `wiki/raw-manifest.md`, read its `doc/` pages, write a source page in `wiki/` plus concept/category updates, then update `wiki/index.md` and `wiki/log.md`.
- **Query** — search `wiki/index.md`, synthesize an answer with citations like `〔PC-034〕`, optionally file it under `wiki/问答/`.
- **Lint** — periodic health-check for contradictions, orphan pages, missing concepts, or gaps fillable by syncing.

Browse with Obsidian (open `wiki/`); start at `wiki/README.md` and `wiki/index.md`.

## Structure

```
xiuliuhe/
  AGENTS.md             <- LLM wiki schema
  catalog.json          <- generated catalog (category→album→episode tree)
  doc/影音/<类别>/<相簿>/<NUM>.md
  wiki/
    SCHEMA.md           <- page templates
    README.md           <- wiki home
    index.md            <- content catalog
    log.md              <- activity log
    raw-manifest.md     <- generated album catalog
    tools/
      api_client.py
      fetch_catalog.py
      download.py
      gen_manifest.py
```
