from pathlib import Path
from datetime import datetime

# ===== 설정 =====
BASE_URL = "https://themoka7.github.io/dev-tools/"   # ← 본인 도메인으로 바꾸세요 (예: https://example.com)
OUTPUT_FILE = "sitemap.xml"

# 프로젝트 루트(이 파일을 실행하는 위치)
root = Path(".")

# 포함할 파일들
targets = []

# 1) index.html
index_file = root / "index.html"
if index_file.exists():
    targets.append(index_file)

# 2) tools 하위의 모든 html
tools_dir = root / "tools"
if tools_dir.exists():
    targets += list(tools_dir.rglob("*.html"))

# 중복 제거 + 정렬
targets = sorted(set(targets))

def to_url(path: Path) -> str:
    rel = path.relative_to(root).as_posix()
    return f"{BASE_URL}/{rel}"

today = datetime.utcnow().strftime("%Y-%m-%d")

# ===== sitemap.xml 생성 =====
lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

for f in targets:
    lines.append("  <url>")
    lines.append(f"    <loc>{to_url(f)}</loc>")
    lines.append(f"    <lastmod>{today}</lastmod>")
    lines.append("  </url>")

lines.append("</urlset>")

Path(OUTPUT_FILE).write_text("\n".join(lines), encoding="utf-8")

print(f"✅ sitemap 생성 완료: {OUTPUT_FILE}")
print(f"총 {len(targets)}개 URL 포함")
