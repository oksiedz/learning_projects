#!/usr/bin/env python3
"""Download a list of all videos in an Internet Archive collection to Excel.

Uses the Internet Archive Advanced Search API (instead of scraping the
details page, which is paginated/lazy-loaded and misses most files) to
enumerate every item in the ``35mmstockfootage`` collection, then fetches
each item's metadata to list its video files and writes name + link to an
Excel spreadsheet.

API reference: https://archive.org/developers/index-apis.html
"""

import argparse
import json
import ssl
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import certifi
from concurrent.futures import ThreadPoolExecutor, as_completed
from openpyxl import Workbook

ADVANCED_SEARCH_URL = "https://archive.org/advancedsearch.php"
ITEM_METADATA_URL = "https://archive.org/metadata/{identifier}"
DOWNLOAD_BASE = "https://archive.org/download/{identifier}"
DETAILS_BASE = "https://archive.org/details/{identifier}"

# Archive item metadata media types that count as video files.
VIDEO_MEDIA_TYPES = {
    "h.264",
    "h264",
    "QuickTime",
    "MPEG-4",
    "MPEG4",
    "Ogg Video",
    "OGV",
    "WebM",
    "Flash Video",
    "AVI",
    "Matroska",
}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".ogv", ".webm", ".flv", ".mpeg", ".mpg"}


def create_ssl_context():
    """Return an SSL context that trusts the certifi CA bundle."""
    return ssl.create_default_context(cafile=certifi.where())


def http_get_json(url, ctx, timeout=30, retries=2, delay=0.5):
    """Fetch JSON from ``url`` with retries and a proper User-Agent."""
    headers = {"User-Agent": "archive-video-list/1.0 (contact: example@example.com)"}
    last_error = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                return json.load(resp)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(delay * (2 ** attempt))
    raise RuntimeError(f"Failed to fetch {url} after {retries + 1} attempts: {last_error}")


def list_item_identifiers(collection, ctx, rows=10000):
    """Yield every item identifier in the given collection.

    Uses a single large request when possible (the Advanced Search API
    reliably returns up to 10000 rows at once). Falls back to paginated
    requests with deduplication if the large request is truncated.
    """
    seen = set()

    def emit_from_page(data):
        docs = data["response"]["docs"]
        for doc in docs:
            ident = doc["identifier"]
            title = doc.get("title")
            # Titles can be a list; normalize to a single string.
            if isinstance(title, list):
                title = " / ".join(str(t) for t in title)
            if ident not in seen:
                seen.add(ident)
                yield ident, title

    # Try to fetch everything in one request.
    params = {
        "q": f"collection:{collection}",
        "fl[]": ["identifier", "title"],
        "rows": rows,
        "start": 0,
        "output": "json",
    }
    url = ADVANCED_SEARCH_URL + "?" + urllib.parse.urlencode(params, doseq=True)
    data = http_get_json(url, ctx)
    num_found = data["response"]["numFound"]
    returned = len(data["response"]["docs"])

    yield from emit_from_page(data)

    # If the single request returned fewer than numFound, paginate through
    # the rest, deduplicating across pages (the collection: query can return
    # duplicates on some pages).
    start = returned
    while start < num_found:
        params["start"] = start
        url = ADVANCED_SEARCH_URL + "?" + urllib.parse.urlencode(params, doseq=True)
        data = http_get_json(url, ctx)
        docs = data["response"]["docs"]
        if not docs:
            break
        yielded_any = False
        for ident, title in emit_from_page(data):
            yielded_any = True
            yield ident, title
        if not yielded_any:
            break
        start += len(docs)


def item_video_files(identifier, ctx):
    """Return a list of (title, filename, download_url, details_url) video files for an item."""
    url = ITEM_METADATA_URL.format(identifier=identifier)
    data = http_get_json(url, ctx)
    metadata = data.get("metadata", {})
    item_title = metadata.get("title") or identifier
    # Archive metadata titles can be a list; normalize to a single string.
    if isinstance(item_title, list):
        item_title = " / ".join(str(t) for t in item_title)
    files = data.get("files", []) or []

    results = []
    for f in files:
        name = f.get("name", "")
        fmt = f.get("format", "")
        # Extract extension from filename
        ext = name[name.rfind("."):].lower() if "." in name else ""

        is_video = fmt in VIDEO_MEDIA_TYPES or ext in VIDEO_EXTENSIONS
        if not is_video:
            continue

        download_url = DOWNLOAD_BASE.format(identifier=identifier) + "/" + name
        details_url = DETAILS_BASE.format(identifier=identifier)
        results.append((item_title, name, download_url, details_url))
    return results


def write_excel(rows, output_path):
    """Write ``[(title, filename, download_url, details_url), ...]`` rows to an Excel file."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Archive Videos"
    ws.append(["Video Title", "File Name", "Download Link", "Details Link"])
    for title, filename, download_url, details_url in rows:
        ws.append([title, filename, download_url, details_url])

    # Set column widths
    widths = [60, 40, 120, 120]
    for idx, width in enumerate(widths, start=1):
        ws.column_dimensions[chr(64 + idx)].width = width

    ws.freeze_panes = "A2"
    wb.save(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="List all videos in an Internet Archive collection to Excel."
    )
    parser.add_argument(
        "--collection", default="35mmstockfootage",
        help="Internet Archive collection identifier (default: 35mmstockfootage)",
    )
    parser.add_argument(
        "--output", default="archive_videos.xlsx",
        help="Output Excel file path (default: archive_videos.xlsx)",
    )
    parser.add_argument(
        "--rows", type=int, default=10000,
        help="Rows per Advanced Search request (default: 10000; "
             "a single large request avoids the API's duplicate pagination bug)",
    )
    parser.add_argument(
        "--workers", type=int, default=10,
        help="Number of parallel workers for metadata requests (default: 10)",
    )
    parser.add_argument(
        "--delay", type=float, default=0.05,
        help="Delay between sequential API calls per worker in seconds (default: 0.05)",
    )
    args = parser.parse_args()

    ctx = create_ssl_context()

    items = list(list_item_identifiers(args.collection, ctx, rows=args.rows))
    identifiers = [ident for ident, _title in items]
    print(f"Found {len(identifiers)} items in collection '{args.collection}'")

    all_rows = []
    completed = {"count": 0}
    lock = threading.Lock()

    def process_one(identifier):
        try:
            videos = item_video_files(identifier, ctx)
            with lock:
                all_rows.extend(videos)
            completed["count"] += 1
            if completed["count"] % 50 == 0:
                with lock:
                    print(f"  Processed {completed['count']}/{len(identifiers)} items, "
                          f"{len(all_rows)} videos collected so far...")
            return identifier, videos, None
        except Exception as exc:  # noqa: BLE001 - keep going on per-item failure
            completed["count"] += 1
            return identifier, [], str(exc)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(process_one, ident): ident for ident in identifiers}
        for future in as_completed(futures):
            future.result()  # propagate any exception but don't crash the loop

    print(f"Total videos found: {len(all_rows)}")
    write_excel(all_rows, args.output)
    print(f"Wrote {len(all_rows)} rows to {args.output}")


if __name__ == "__main__":
    main()