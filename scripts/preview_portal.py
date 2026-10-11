"""Local root-home preview, with a read-only mapping to the existing article site."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
ARTICLES = ROOT.parent / "GitHub公开定稿" / "_site"

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, articles_site, **kwargs):
        self.articles_site = articles_site
        super().__init__(*args, **kwargs)

    def translate_path(self, path):
        decoded = unquote(urlsplit(path).path)
        if decoded == "/articles":
            decoded = "/articles/"
        if decoded.startswith("/articles/"):
            base = self.articles_site
            relative = decoded[len("/articles/"):]
        else:
            base = DIST
            relative = decoded.lstrip("/")
        target = (base / relative).resolve()
        if not target.is_relative_to(base) or any(part.startswith(".") for part in Path(relative).parts):
            return str(DIST / "__not_served__")
        return str(target)

    def list_directory(self, path):
        self.send_error(403, "Directory listing is disabled.")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--articles-site", type=Path, default=ARTICLES)
    args = parser.parse_args()
    article_site = args.articles_site.resolve()
    if DIST.is_symlink() or DIST.resolve() != ROOT.resolve() / "dist" or not (DIST / "index.html").is_file():
        parser.error("The root home dist/index.html is missing or unsafe.")
    if args.articles_site.is_symlink() or not (article_site / ".generated-by-blog").is_file():
        parser.error("Use the existing generated article _site directory.")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(Handler, directory=str(DIST), articles_site=article_site))
    print(f"Local root home: http://127.0.0.1:{args.port}/", flush=True)
    print("Only dist and the existing generated article site are served. Ctrl+C stops.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
