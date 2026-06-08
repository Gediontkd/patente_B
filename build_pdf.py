#!/usr/bin/env python3
"""
Reusable PDF builder for Patente B study notes.
Each section is defined as a Python dict and rendered to a clean, styled PDF.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

# ---- Black + dark navy accent palette ----
NAVY = colors.HexColor("#1F3A5F")   # single accent color
RED = NAVY        # headings / titles use the accent
GREEN = NAVY      # subtitle / hints use the accent
DARK = colors.black   # all body text stays black
LIGHT = colors.white
ACCENT = NAVY

styles = getSampleStyleSheet()

title_style = ParagraphStyle("TitleX", parent=styles["Title"],
    fontSize=26, textColor=RED, spaceAfter=2, alignment=TA_CENTER, leading=30)
subtitle_style = ParagraphStyle("SubX", parent=styles["Normal"],
    fontSize=13, textColor=GREEN, alignment=TA_CENTER, spaceAfter=14,
    fontName="Helvetica-Oblique")
h2 = ParagraphStyle("H2X", parent=styles["Heading2"],
    fontSize=15, textColor=RED, spaceBefore=14, spaceAfter=6, fontName="Helvetica-Bold")
body = ParagraphStyle("BodyX", parent=styles["Normal"],
    fontSize=11, textColor=DARK, leading=16, spaceAfter=6)
bullet = ParagraphStyle("BulletX", parent=body, leftIndent=14, bulletIndent=2)
quote = ParagraphStyle("QuoteX", parent=styles["Normal"],
    fontSize=9.5, textColor=colors.black, leftIndent=10,
    fontName="Helvetica-Oblique", leading=13, spaceAfter=6)
cell = ParagraphStyle("CellX", parent=styles["Normal"], fontSize=10, leading=13)
cell_b = ParagraphStyle("CellB", parent=cell, fontName="Helvetica-Bold")
cell_h = ParagraphStyle("CellH", parent=cell, fontName="Helvetica-Bold",
    textColor=colors.white)
hint = ParagraphStyle("HintX", parent=body, textColor=GREEN, fontName="Helvetica-Bold")


def build_section(section, out_path):
    doc = SimpleDocTemplate(out_path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm,
        title=section["title"])
    flow = []

    flow.append(Paragraph(section["title"], title_style))
    if section.get("subtitle"):
        flow.append(Paragraph(section["subtitle"], subtitle_style))
    flow.append(HRFlowable(width="100%", thickness=2, color=GREEN, spaceAfter=10))

    for block in section["blocks"]:
        t = block["type"]
        if t == "h2":
            flow.append(Paragraph(block["text"], h2))
        elif t == "para":
            flow.append(Paragraph(block["text"], body))
        elif t == "quote":
            flow.append(Paragraph(block["text"], quote))
        elif t == "hint":
            flow.append(Paragraph(block["text"], hint))
        elif t == "bullets":
            for b in block["items"]:
                flow.append(Paragraph("&bull;&nbsp;&nbsp;" + b, bullet))
        elif t == "table":
            data = []
            header = [Paragraph(h, cell_h) for h in block["headers"]]
            data.append(header)
            for row in block["rows"]:
                data.append([Paragraph(c, cell) for c in row])
            ncols = len(block["headers"])
            widths = block.get("widths") or [doc.width/ncols]*ncols
            tbl = Table(data, colWidths=widths, repeatRows=1)
            tbl.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), NAVY),
                ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
                ("LINEBELOW", (0,0), (-1,0), 1.5, NAVY),
                ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#EEF1F5")]),
                ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#AAB4C0")),
                ("VALIGN", (0,0), (-1,-1), "TOP"),
                ("LEFTPADDING", (0,0), (-1,-1), 6),
                ("RIGHTPADDING", (0,0), (-1,-1), 6),
                ("TOPPADDING", (0,0), (-1,-1), 5),
                ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ]))
            flow.append(tbl)
            flow.append(Spacer(1, 6))
        elif t == "spacer":
            flow.append(Spacer(1, block.get("h", 10)))
        elif t == "rule":
            flow.append(HRFlowable(width="100%", thickness=1,
                color=colors.black, spaceBefore=6, spaceAfter=6))

    doc.build(flow)
    print(f"Created: {out_path}")
