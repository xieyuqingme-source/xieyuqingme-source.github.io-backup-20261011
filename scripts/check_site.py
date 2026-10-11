"""Check the root home's actual files and links, without a browser or network."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree
import argparse, json

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
class Elements(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.elements = []; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

def check(article_site):
    page = Elements((DIST / "index.html").read_text(encoding="utf-8"))
    ids = [a["id"] for _,a in page.elements if "id" in a]
    assert len(ids) == len(set(ids))
    assert sum(tag == "h1" for tag,_ in page.elements) == 1
    assert any(tag == "meta" and a.get("name") == "viewport" for tag,a in page.elements)
    urls = [a[key] for _,a in page.elements for key in ("href","src") if a.get(key)]
    checked = []; recent_paths = []
    for url in urls:
        parsed = urlsplit(url)
        assert not parsed.scheme or parsed.scheme == "https", url
        if parsed.netloc and parsed.netloc != "xieyuqingme-source.github.io":
            continue
        if parsed.path.startswith("/articles/"):
            base = article_site; relative = unquote(parsed.path[len("/articles/"):])
        else:
            base = DIST; relative = unquote(parsed.path).lstrip("/")
        target = (base / relative).resolve()
        assert target.is_relative_to(base) and target.exists(), url
        if target.is_dir(): target = target / "index.html"
        assert target.is_file(), url
        if parsed.fragment:
            assert target == DIST / "index.html" and unquote(parsed.fragment) in ids, url
        checked.append(url)
        if relative.startswith(("中文文章/", "English Articles/")) and relative.endswith(".html"):
            recent_paths.append(relative)
    dates = [a["datetime"] for tag,a in page.elements if tag == "time"]
    metadata_path = article_site.parent / "blog/publication-dates.json"
    if metadata_path.is_file():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        assert len(metadata) == 117
        assert len(recent_paths) == len(dates) == 3
        for relative,day in zip(recent_paths,dates):
            assert metadata[str(Path(relative).with_suffix(".md")).replace("\\","/")]["date"] == day
    sitemap = ElementTree.parse(DIST / "sitemap.xml")
    assert sitemap.find(".//{*}loc").text == "https://xieyuqingme-source.github.io/"
    assert 'Sitemap: https://xieyuqingme-source.github.io/sitemap.xml' in (DIST / "robots.txt").read_text(encoding="utf-8")
    assert (DIST / ".nojekyll").is_file()
    return {"success": True, "local_links_checked": len(checked), "recent_articles": 3, "recent_dates_match_article_metadata": True,
            "root_canonical": "https://xieyuqingme-source.github.io/", "article_column": "/articles/", "links": checked,
            "browser_rendering_checked": False, "network_actions_performed": False}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--articles-site", type=Path, default=ROOT.parent / "GitHub公开定稿/_site")
    args = parser.parse_args()
    print(json.dumps(check(args.articles_site.resolve()),ensure_ascii=False,indent=2))
