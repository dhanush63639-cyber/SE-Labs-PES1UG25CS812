"""Build the consolidated Lab 5 PDF report from verified project results."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "LAB5_PES1UG25CS812_Report.pdf"


def build_report() -> None:
    """Create the submission report PDF."""
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CoverTitle", parent=styles["Title"], fontSize=22,
        leading=28, alignment=TA_CENTER, textColor=colors.HexColor("#16324F"),
    ))
    styles.add(ParagraphStyle(
        name="SubCenter", parent=styles["Normal"], fontSize=11,
        leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#526579"),
    ))
    styles.add(ParagraphStyle(
        name="Section", parent=styles["Heading2"], fontSize=14,
        textColor=colors.HexColor("#16324F"), spaceBefore=12, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="BodySmall", parent=styles["BodyText"], fontSize=9.5,
        leading=14, spaceAfter=6,
    ))

    story = [
        Spacer(1, 15 * mm),
        Paragraph("LAB 5 — STATIC CODE ANALYSIS", styles["CoverTitle"]),
        Paragraph("Retail Point of Sale &amp; Discount Tracker", styles["SubCenter"]),
        Spacer(1, 10 * mm),
    ]
    meta = [
        ["Student", "Dhanush Gowda A S"],
        ["SRN", "PES1UG25CS812"],
        ["Repository", "SE-Labs-PES1UG25CS812"],
        ["Folder", "LAB5_PES1UG25CS812"],
    ]
    table = Table(meta, colWidths=[42 * mm, 112 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF0F6")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#16324F")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9D4DF")),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story += [table, Spacer(1, 8 * mm)]

    sections = [
        ("1. Objective",
         "Analyze the supplied Retail POS starter program using Pylint, Bandit and "
         "Flake8; document defects, remediate the implementation, and compare "
         "static-analysis results before and after the changes."),
        ("2. Tools",
         "<b>Pylint</b> — Python code-quality diagnostics.<br/>"
         "<b>Bandit</b> — security-focused static analysis.<br/>"
         "<b>Flake8</b> — style and lint checks.<br/>"
         "<b>unittest</b> — regression tests for checkout, validation, promotions, "
         "inventory and receipt logging."),
    ]
    for heading, body in sections:
        story += [Paragraph(heading, styles["Section"]),
                  Paragraph(body, styles["BodySmall"])]

    story.append(Paragraph("3. Before-and-after results", styles["Section"]))
    results = [
        ["Analyzer", "Before", "After"],
        ["Pylint", "5.78 / 10", "10.00 / 10"],
        ["Bandit", "3 findings (2 Low, 1 Medium)", "No findings reported"],
        ["Flake8", "Multiple violations", "No violations reported"],
        ["Regression tests", "Baseline defects present", "Passed in GitHub Actions"],
    ]
    result_table = Table(results, colWidths=[35 * mm, 61 * mm, 61 * mm], repeatRows=1)
    result_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16324F")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9D4DF")),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F7F9FB")),
        ("PADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(result_table)

    story.append(Paragraph("4. Issues identified and fixes", styles["Section"]))
    fixes = [
        ("Unsafe eval()", "Replaced arbitrary expression evaluation with allow-listed promo codes."),
        ("Mutable default argument", "Replaced shared receipts=[] with None and per-call handling."),
        ("Broad exception handling", "Added explicit validation and meaningful exceptions."),
        ("Invalid cart inputs", "Rejects unknown products, invalid quantities and invalid tax rates."),
        ("Stock update defect", "Implemented validated inventory quantity updates."),
        ("Unmanaged file handling", "Uses a context manager and UTF-8 encoding."),
        ("Style and maintainability", "Applied snake_case naming, documentation and consistent formatting."),
    ]
    for title, description in fixes:
        story.append(Paragraph(f"<b>{title}:</b> {description}", styles["BodySmall"]))

    story.append(Paragraph("5. Validation and reproducibility", styles["Section"]))
    story.append(Paragraph(
        "The repository's GitHub Actions run completed successfully: dependencies "
        "were installed, regression tests passed, and the six before/after analyzer "
        "reports were generated and committed. The corrected source achieved a "
        "Pylint score of 10.00/10, with no Bandit findings and no Flake8 violations.",
        styles["BodySmall"]))
    story.append(Paragraph(
        "To reproduce locally, run <font name='Courier'>python -m pip install -r "
        "requirements.txt</font>, <font name='Courier'>python -m unittest discover "
        "-s tests -v</font>, and <font name='Courier'>python run_analysis.py</font>.",
        styles["BodySmall"]))

    story.append(Paragraph("6. Deliverables", styles["Section"]))
    story.append(Paragraph(
        "The folder contains the original baseline source, corrected source, issue "
        "register, reflection, README, analysis runner, requirements, regression "
        "tests, six analyzer output files and this PDF report.", styles["BodySmall"]))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(
        "This is the project report, not a replacement for any separate official "
        "lab handout or template issued by the instructor.", styles["BodySmall"]))

    def footer(canvas, document):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D7E0E8"))
        canvas.line(20 * mm, 14 * mm, A4[0] - 20 * mm, 14 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#64748B"))
        canvas.drawString(20 * mm, 9 * mm, "LAB 5 — Static Code Analysis")
        canvas.drawRightString(A4[0] - 20 * mm, 9 * mm, f"Page {document.page}")
        canvas.restoreState()

    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm,
    )
    document.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build_report()
    print(f"Created {OUTPUT.name}")
