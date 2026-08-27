"""Python client for the xiuliuhe (m.xiuliuhe.org) public API.

Provides the `api` namespace and URL builders used by the sync tools. Mirrors
the pattern from xwcz's api_client.py but targets https://m.xiuliuhe.org/api/.

Media hosts reverse-engineered from https://m.xiuliuhe.org/js/app.*.js:
  function m(e,t,n) = host + major + "/" + major-minor + "/" (+t+"/" if m3u8) + t + "." + n
  where t is NUM like PC-034-0001, e is host like https://s.liuhejing.cc/
  and n is ext (mp4/m3u8/mp3/jpg).

Actual media folders used by xiuliuhe are mp4/mp3/m3u8/image (verified via HEAD):
  https://s.liuhejing.cc/mp4/PC/PC-034/PC-034-0001.mp4
  https://s.liuhejing.cc/mp3/PC/PC-034/PC-034-0001.mp3
  https://s.liuhejing.cc/m3u8/PC/PC-034/PC-034-0001/PC-034-0001.m3u8
  https://s.liuhejing.cc/image/PC/PC-034/PC-034-0001.jpg
"""

import json
import urllib.parse
import urllib.request

API_BASE_URL = "https://m.xiuliuhe.org/api/"

MEDIA_HOSTS = {
    "primary": "https://s.liuhejing.cc/",
    "backup": "https://d.liuhejing.cc/",
}

DEFAULT_PARAMS = {}  # xiuliuhe API currently takes no default client=v params


class XiuLiuHeApiError(RuntimeError):
    pass


def request(path, params=None, base_url=API_BASE_URL):
    """GET a xiuliuhe API endpoint, returning the parsed JSON payload."""
    merged = dict(DEFAULT_PARAMS)
    if params:
        merged.update({k: str(v) for k, v in params.items() if v not in (None, "", 0, [])})
    url = urllib.parse.urljoin(base_url, path) + (
        "?" + urllib.parse.urlencode(merged) if merged else ""
    )
    with urllib.request.urlopen(url, timeout=60) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if payload.get("code") and payload.get("code") != 200:
        raise XiuLiuHeApiError(
            "xiuliuhe API {}: {}".format(payload["code"], payload.get("msg") or path)
        )
    return payload


def category_list(cid=None):
    return request("category/list", {"cid": cid})


def album_list(cid, page=1):
    return request("album/list", {"cid": cid, "page": page})


def video_list(aid):
    return request("video/list", {"aid": aid})


def video_detail(eid):
    return request("video/detail", {"id": eid})


def article_detail(eid):
    return request("article/detail", {"id": eid})


api = {
    "categoryList": category_list,
    "albumList": album_list,
    "videoList": video_list,
    "videoDetail": video_detail,
    "articleDetail": article_detail,
}


def _split_num(num):
    if not num:
        return None, None
    parts = str(num).split("-")
    if len(parts) < 2:
        return None, None
    return parts[0], parts[1]


def build_numbered_asset_url(host, folder, num, ext):
    """Build the xiuliuhe media asset URL for a numbered code.

    e.g. build_numbered_asset_url('https://s.liuhejing.cc/', 'mp4', 'PC-034-0001', 'mp4')
         -> https://s.liuhejing.cc/mp4/PC/PC-034/PC-034-0001.mp4
    """
    if not num:
        return ""
    major, minor = _split_num(num)
    if not major or not minor:
        return ""
    base = "{}{}/{}/{}-{}/".format(host, folder, major, major, minor)
    if ext == "m3u8":
        return "{}{}/{}.{}".format(base, num, num, ext)
    return "{}{}.{}".format(base, num, ext)


def get_video_mp4_url(num, host=MEDIA_HOSTS["primary"]):
    return build_numbered_asset_url(host, "mp4", num, "mp4")


def get_video_hls_url(num, host=MEDIA_HOSTS["primary"]):
    return build_numbered_asset_url(host, "m3u8", num, "m3u8")


def get_audio_mp3_url(num, host=MEDIA_HOSTS["primary"]):
    return build_numbered_asset_url(host, "mp3", num, "mp3")


def get_poster_url(num, host=MEDIA_HOSTS["primary"]):
    return build_numbered_asset_url(host, "image", num, "jpg")
