"""Narrow mmdc 12 adapter: use allowed local HTTP for its HTML shell."""

from pathlib import Path
import sys

path = Path(sys.argv[1])
original = "await page.goto(url.pathToFileURL(mermaidHTMLPath).href);"
adapted = "await page.goto(process.env.MMDC_RENDER_HTML_URL || url.pathToFileURL(mermaidHTMLPath).href);"
source = path.read_text()
before, after = (adapted, original) if "--restore" in sys.argv[2:] else (original, adapted)
if source.count(after) == 1 and source.count(before) == 0:
    pass
elif source.count(before) == 1 and source.count(after) == 0:
    path.write_text(source.replace(before, after))
else:
    raise SystemExit("Unsupported Mermaid CLI source; refusing an ambiguous compatibility patch")
