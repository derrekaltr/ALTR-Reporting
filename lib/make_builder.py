import sys, ast, re
from pathlib import Path
slug, name, handle, datestr, pdfname = sys.argv[1:6]
root = Path.home() / "Documents/altr-reports-kit"
s = (root / "WORK/liza-weekly/build_premium.py").read_text()
s = s.replace('"""Liza Kovalenko. Weekly report, creator-facing. Built October 14, 2026.',
              f'"""{name}. Weekly report, creator-facing. Built {datestr}.')
s = s.replace('NAME = "Liza Kovalenko"; FIRST = NAME.split()[0]; HANDLE = "@lizakovalenkoo"',
              f'NAME = "{name}"; FIRST = NAME.split()[0]; HANDLE = "@{handle}"')
s = re.sub(r'DATE = "[^"]+"', f'DATE = "{datestr}"', s, count=1)
s = re.sub(r'PDF = "[^"]+"', f'PDF = "{pdfname}"', s, count=1)
s = s.replace('October 7 to 13', 'October 8 to 14')
lines = s.split("\n")
h = next(i for i, l in enumerate(lines) if l.startswith("HOOK = "))
j = next(i for i, l in enumerate(lines) if l.startswith("STORY_X"))
while not lines[j].rstrip().endswith("]"):
    j += 1
prose = (root / "WORK" / slug / "prose.py").read_text()
lines[h:j + 1] = [prose]
out = "\n".join(lines)
ast.parse(out)
(root / "WORK" / slug / "build_premium.py").write_text(out)
print(f"builder written: WORK/{slug}/build_premium.py")
