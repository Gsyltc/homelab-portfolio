# Export PDF

- Le PDF `sport/programme-sportif.pdf` est généré **uniquement lorsque le programme a évolué** (après validation humaine + validation du chef de clinique et application), jamais sur simple lecture.
- Le déposer en pièce jointe (attachment) sur l'issue pour téléchargement.
- Génération avec Python `fpdf2` (disponible dans l'environnement). Adapter `<patient>` et vérifier le rendu avant dépôt.

```python
import re
from fpdf import FPDF

SRC = "$ROOT_DIRECTORY/<patient>/sport/programme-sportif.md"
OUT = "$ROOT_DIRECTORY/<patient>/sport/programme-sportif.pdf"

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("helvetica", "B", 14)
pdf.cell(0, 10, "Programme sportif", new_x="LMARGIN", new_y="NEXT")


def add_md_lines(pdf, lines):
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if any(re.sub(r"[-:]+", "", c).strip() for c in cells):
                pdf.set_font("helvetica", "B", 9)
                for c in cells:
                    pdf.cell(0 if len(cells) == 1 else 35, 6, c[:60], border=1)
                pdf.ln()
        elif line.startswith("##"):
            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 8, line.lstrip("#").strip(), new_x="LMARGIN", new_y="NEXT")
        elif line.startswith("#"):
            pdf.set_font("helvetica", "B", 13)
            pdf.cell(0, 9, line.lstrip("#").strip(), new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.set_font("helvetica", "", 10)
            pdf.multi_cell(0, 5, line.strip(), new_x="LMARGIN", new_y="NEXT")


with open(SRC, encoding="utf-8") as fh:
    add_md_lines(pdf, fh.readlines())

pdf.output(OUT)
print("PDF généré:", OUT)
```
