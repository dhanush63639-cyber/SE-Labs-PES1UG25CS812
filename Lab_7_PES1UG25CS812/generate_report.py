"""Generate Lab 7 terminal evidence screenshots and a PDF report from real test runs."""
from pathlib import Path
import re
import subprocess
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as PDFImage, PageBreak

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "screenshots"
EVIDENCE.mkdir(exist_ok=True)
BEFORE = ROOT / "evidence" / "before_fix"


def execute(command, cwd):
    result = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return result.returncode, result.stdout


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def make_terminal_capture(filename, title, command, output, max_lines=30):
    mono = font("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)
    mono_bold = font("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 19)
    width, margin, line_height = 1600, 34, 27
    lines = [f"$ {command}"]
    lines.extend(output.strip().splitlines() or ["(no output)"])
    wrapped = []
    max_chars = 126
    for line in lines:
        wrapped.extend(textwrap.wrap(line, width=max_chars, subsequent_indent="    ") or [""])
    if len(wrapped) > max_lines:
        wrapped = wrapped[:max_lines - 2] + ["...", *wrapped[-2:]]
    height = 100 + len(wrapped) * line_height + 30
    image = Image.new("RGB", (width, height), (18, 22, 28))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((12, 12, width - 12, height - 12), radius=16,
                           fill=(24, 29, 37), outline=(74, 86, 101), width=2)
    draw.rounded_rectangle((12, 12, width - 12, 72), radius=16, fill=(39, 47, 59))
    for x, color in [(35, (239, 83, 80)), (64, (255, 190, 60)), (93, (76, 175, 80))]:
        draw.ellipse((x, 34, x + 15, 49), fill=color)
    draw.text((130, 27), title, font=mono_bold, fill=(235, 240, 247))
    y = 88
    for line in wrapped:
        color = (225, 231, 239)
        if "FAILED" in line or "ERROR" in line or "failed" in line:
            color = (255, 151, 151)
        elif "PASSED" in line or "passed" in line or "Sanitized Plate" in line or "Parsed Mileage" in line or "Rental Invoice" in line:
            color = (145, 224, 166)
        draw.text((margin, y), line, font=mono, fill=color)
        y += line_height
    path = EVIDENCE / filename
    image.save(path)
    return path


def add_image(story, path):
    from PIL import Image as PILImage
    with PILImage.open(path) as im:
        ratio = im.height / im.width
    story.append(PDFImage(str(path), width=175 * mm, height=175 * mm * ratio))


def main():
    original_demo_code, original_demo = execute([sys.executable, "processor.py"], BEFORE)
    baseline_code, baseline = execute(
        [sys.executable, "-m", "pytest", "-v", "test_processor.py", "--tb=short"], BEFORE
    )
    fixed_demo_code, fixed_demo = execute([sys.executable, "processor.py"], ROOT)
    fixed_test_code, fixed_tests = execute(
        [sys.executable, "-m", "pytest", "-v", "test_processor.py"], ROOT
    )

    if original_demo_code != 0 or baseline_code == 0 or fixed_demo_code != 0 or fixed_test_code != 0:
        raise SystemExit("Evidence generation stopped: expected before/after execution results were not observed.")

    baseline_summary = re.search(r"=+\s*(\d+ failed, \d+ passed in [\d.]+s)\s*=+", baseline)
    fixed_summary = re.search(r"=+\s*(\d+ passed in [\d.]+s)\s*=+", fixed_tests)
    if not baseline_summary or not fixed_summary:
        raise SystemExit("Could not parse pytest summaries; report was not generated.")

    baseline_lines = [
        line for line in baseline.splitlines()
        if "FAILED " in line or "Hypothesis found" in line or "AttributeError" in line
        or "IndexError" in line or "DID NOT RAISE" in line
        or "short test summary" in line or re.search(r"\d+ failed, \d+ passed", line)
    ]
    baseline_excerpt = "\n".join(baseline_lines[-18:])

    p1 = make_terminal_capture("step2_original_processor.png", "Step 2 — Original processor output",
                               "python processor.py", original_demo)
    p2 = make_terminal_capture("step4_fuzz_failures.png", "Step 4 — Fuzz tests before fixes",
                               "python -m pytest -v test_processor.py", baseline_excerpt, max_lines=24)
    p3 = make_terminal_capture("step5_fixed_processor.png", "Step 5 — Hardened processor output",
                               "python processor.py", fixed_demo)
    p4 = make_terminal_capture("step6_passing_tests.png", "Step 6 — Fuzz tests after fixes",
                               "python -m pytest -v test_processor.py", fixed_tests, max_lines=28)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="LabBody", parent=styles["BodyText"], fontSize=9, leading=13))
    styles.add(ParagraphStyle(name="LabSub", parent=styles["Normal"], fontSize=10, leading=14,
                              textColor=colors.HexColor("#465466")))
    styles.add(ParagraphStyle(name="LabSection", parent=styles["Heading2"], fontSize=15,
                              leading=18, textColor=colors.HexColor("#17365D"),
                              spaceBefore=4, spaceAfter=7))
    pdf_path = ROOT / "LAB7_FuzzTesting_Report.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=17*mm,
                            leftMargin=17*mm, topMargin=15*mm, bottomMargin=15*mm)
    story = [
        Paragraph("LAB 7: FUZZING FOR INPUT VALIDATION BUGS", styles["Title"]),
        Paragraph("Student: Dhanush Gowda A S &nbsp; | &nbsp; USN: PES1UG25CS812", styles["LabSub"]),
        Paragraph("Project: Car Rental Rate &nbsp; | &nbsp; Python + Hypothesis", styles["LabSub"]),
        Spacer(1, 7*mm),
        Paragraph("Objective", styles["LabSection"]),
        Paragraph("Follow the supplied student handout: run the original application, use Hypothesis to discover edge cases in all three functions, fix the validation defects, and rerun the tests.", styles["LabBody"]),
        Paragraph("Functions tested", styles["LabSection"]),
        Paragraph("<b>sanitize_license_plate()</b> — normalize a license plate and remove supported delimiters.<br/><b>parse_trip_mileage()</b> — parse comma-separated mileage values as floats.<br/><b>format_rental_invoice()</b> — parse Driver:Days:Category and calculate the rental total.", styles["LabBody"]),
        Paragraph("Step 1 — Dependencies", styles["LabSection"]),
        Paragraph("The CI runner installed pytest and Hypothesis from requirements.txt under Python 3.12.16. The test framework and fuzzing library were installed before running the original and fixed versions.", styles["LabBody"]),
        Paragraph("Step 2 — Original application output", styles["LabSection"]),
        Paragraph("The starter program completed with ordinary sample inputs. Its successful normal-path output did not cover malformed or unexpected values.", styles["LabBody"]),
    ]
    add_image(story, p1)
    story += [
        PageBreak(),
        Paragraph("Steps 3–4 — Hypothesis fuzzing and initial failures", styles["LabSection"]),
        Paragraph("The property-based tests generated strings, None values and integers for each function. Additional regression cases checked empty and invalid plates, empty/nonnumeric/negative/non-finite mileage, malformed invoice records, and non-positive rental days.", styles["LabBody"]),
    ]
    add_image(story, p2)
    story += [
        Spacer(1, 3*mm),
        Paragraph(f"<b>Baseline outcome:</b> {baseline_summary.group(1)}. The original implementation leaked AttributeError/IndexError and accepted invalid plate characters, negative or non-finite mileage, and zero/negative rental days.", styles["LabBody"]),
        PageBreak(),
        Paragraph("Step 5 — Hardened application", styles["LabSection"]),
        Paragraph("Input types and structure are validated before processing. Wrong types raise TypeError; invalid values raise ValueError rather than leaking incidental parser exceptions.", styles["LabBody"]),
        Paragraph("Fixes applied", styles["LabSection"]),
        Paragraph("• License plates must be non-empty and alphanumeric after supported separators are removed.<br/>• Mileage entries must be numeric, finite and non-negative; empty CSV fields are rejected.<br/>• Rental records must contain exactly three fields, a non-empty driver and category, and a positive integer day count.<br/>• Existing pricing is preserved: SUV $50/day; other categories $30/day.", styles["LabBody"]),
    ]
    add_image(story, p3)
    story += [
        PageBreak(),
        Paragraph("Step 6 — Final test execution", styles["LabSection"]),
        Paragraph("The same fuzz and regression suite was executed against the fixed processor. The result below is taken from the successful pytest run.", styles["LabBody"]),
    ]
    add_image(story, p4)
    story += [
        Spacer(1, 4*mm),
        Paragraph(f"<b>Final outcome:</b> {fixed_summary.group(1)}. All three Hypothesis fuzz tests and all deterministic regression tests passed.", styles["LabBody"]),
        Paragraph("Conclusion", styles["LabSection"]),
        Paragraph("The before-and-after runs demonstrate that fuzzing exposed real input-validation defects and that the hardened implementation now handles the tested valid and invalid inputs consistently.", styles["LabBody"]),
    ]
    doc.build(story)
    print(f"Generated {pdf_path}")
    print(f"Baseline: {baseline_summary.group(1)}")
    print(f"Fixed: {fixed_summary.group(1)}")


if __name__ == "__main__":
    main()
