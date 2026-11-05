import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "PES University — UE23CS352B Software Engineering Lab")
            self.drawRightString(612 - 54, 750, "Lab 7: Fuzzing for Input Validation Bugs")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(54, 742, 612 - 54, 742)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 45, 612 - 54, 45)
        self.drawString(54, 32, "Krrish P Raju (PES1UG24CS708) — Section L — Problem #44 Scholarship Awards")
        self.drawRightString(612 - 54, 32, f"Page {self._pageNumber} of {total_pages}")
        self.restoreState()

def create_report():
    pdf_path = "Lab7_Fuzzing_Report_PES1UG24CS708.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#0F172A")    # slate 900
    accent_color = colors.HexColor("#2563EB")     # blue 600
    secondary_color = colors.HexColor("#475569")  # slate 600

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        alignment=1, # Center
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=accent_color,
        alignment=1,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=accent_color,
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6
    )

    caption_style = ParagraphStyle(
        'ImgCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=secondary_color,
        alignment=1,
        spaceBefore=4,
        spaceAfter=10
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F1F5F9"),
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    story = []

    # Title & Header
    story.append(Paragraph("PES UNIVERSITY", ParagraphStyle('PES', fontName='Helvetica-Bold', fontSize=14, leading=16, alignment=1, textColor=colors.HexColor("#1E3A8A"))))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", ParagraphStyle('Dept', fontName='Helvetica-Bold', fontSize=10, leading=12, alignment=1, textColor=secondary_color, spaceAfter=8)))
    story.append(Paragraph("LABORATORY REPORT — LAB 7", title_style))
    story.append(Paragraph("Fuzzing for Input Validation Bugs using Hypothesis", subtitle_style))

    # Student Metadata Table
    meta_data = [
        [
            Paragraph("<b>Student Name:</b> Krrish P Raju", body_style),
            Paragraph("<b>SRN:</b> PES1UG24CS708", body_style)
        ],
        [
            Paragraph("<b>Course:</b> UE23CS352B — Software Engineering Lab", body_style),
            Paragraph("<b>Section:</b> L", body_style)
        ],
        [
            Paragraph("<b>Assigned Problem:</b> #44 Scholarship Awards", body_style),
            Paragraph("<b>Date of Submission:</b> November 5, 2026", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[260, 244])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Objective & Concepts
    story.append(Paragraph("1. Objective & Methodological Background", h1_style))
    story.append(Paragraph(
        "The objective of this laboratory exercise is to explore <b>fuzz testing</b> as a dynamic security and quality assurance technique. "
        "Unlike traditional manual or unit testing—which only exercises known assumptions and anticipated paths—fuzzing automatically generates "
        "pseudo-random, malformed, and boundary-value inputs to uncover hidden input validation vulnerabilities, crashes, uncaught exceptions, "
        "and security flaws.",
        body_style
    ))
    story.append(Paragraph(
        "Using Python's <b>Hypothesis</b> property-based testing framework, we specify broad input strategies (such as <code>st.text() | st.none()</code>) "
        "and assert functional invariants (such as 'the application must never crash regardless of input'). Hypothesis tests hundreds of inputs, "
        "automatically detects failures, and <i>shrinks</i> failing cases down to their minimal reproducible counterexamples.",
        body_style
    ))

    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#E2E8F0"), spaceBefore=6, spaceAfter=8))

    # Step 2: Running the Buggy Application
    story.append(Paragraph("2. Step 2: Execution of Buggy Application", h1_style))
    story.append(Paragraph(
        "The starter Python module (<code>scholarship_awards.py</code> / <code>processor.py</code>) processes applicant categories and marks, "
        "computes average marks from CSV input, and determines payable awards after tax multiplier and deductions. "
        "Executing the application under normal, cooperative user inputs yields the expected outputs without errors:",
        body_style
    ))

    # Step 2 Image
    img_w = 480
    img_h_step2 = img_w * (396 / 1000)
    story.append(Image("step2_run_buggy_processor.png", width=img_w, height=img_h_step2))
    story.append(Paragraph("<b>Figure 1:</b> Step 2 — Initial execution of buggy processor with standard sample inputs.", caption_style))

    story.append(PageBreak())

    # Step 3 & 4: Hypothesis Fuzz Testing & Failures
    story.append(Paragraph("3. Step 3 & 4: Hypothesis Fuzz Testing and Discovered Bugs", h1_style))
    story.append(Paragraph(
        "We implemented property-based tests in <code>test_processor.py</code> using Hypothesis strategies <code>st.text() | st.none()</code>. "
        "The property under test asserts that neither <code>parse_applicant</code>, <code>marks_average</code>, nor <code>payable_award</code> "
        "should terminate with an unhandled exception upon receiving malformed input.",
        body_style
    ))

    test_snippet = (
        "@given(st.text() | st.none())\n"
        "def test_parse_applicant_no_crash(s):\n"
        "    try:\n"
        "        parse_applicant(s)\n"
        "    except Exception as e:\n"
        "        assert False, f'parse_applicant crashed with: {e}'\n"
    )
    story.append(Paragraph(test_snippet.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

    story.append(Paragraph(
        "Running <code>pytest test_processor.py</code> against the buggy implementation exposed multiple critical crashes across all three functions. "
        "Hypothesis immediately identified minimal failing examples, demonstrating how unvalidated inputs lead to application termination:",
        body_style
    ))

    # Step 4 Image
    img_h_step4 = img_w * (928 / 1040)
    story.append(Image("step4_pytest_fuzzing_failures.png", width=img_w, height=img_h_step4))
    story.append(Paragraph("<b>Figure 2:</b> Step 4 — Pytest execution exposing crashes and minimal falsifying examples discovered by Hypothesis.", caption_style))

    story.append(PageBreak())

    # Bug Breakdown Table
    story.append(Paragraph("4. Bug Analysis & Root Causes", h1_style))
    bugs_data = [
        [
            Paragraph("<b>Target Function</b>", body_style),
            Paragraph("<b>Hypothesis Minimal Falsifier</b>", body_style),
            Paragraph("<b>Exception Type</b>", body_style),
            Paragraph("<b>Root Cause Analysis</b>", body_style)
        ],
        [
            Paragraph("<code>parse_applicant(text)</code>", body_style),
            Paragraph("<code>s = None</code><br/><code>s = ''</code>", body_style),
            Paragraph("<code>AttributeError</code><br/><code>ValueError</code>", body_style),
            Paragraph("Calling <code>.split(':')</code> on <code>None</code> raises AttributeError; splitting strings without colon raises ValueError (too few elements to unpack).", body_style)
        ],
        [
            Paragraph("<code>marks_average(marks_csv)</code>", body_style),
            Paragraph("<code>s = ''</code><br/><code>s = None</code>", body_style),
            Paragraph("<code>ValueError</code><br/><code>AttributeError</code>", body_style),
            Paragraph("Splitting empty string yields <code>['']</code>, causing <code>int('')</code> to raise ValueError. Passing <code>None</code> raises AttributeError. Empty token causes ZeroDivisionError.", body_style)
        ],
        [
            Paragraph("<code>payable_award(text)</code>", body_style),
            Paragraph("<code>s = '|'</code><br/><code>s = ''</code><br/><code>s = None</code>", body_style),
            Paragraph("<code>ValueError</code><br/><code>AttributeError</code>", body_style),
            Paragraph("Empty parts around pipe delimiter cause <code>float('')</code> to raise ValueError. Missing pipe causes unpack error. Passing <code>None</code> causes AttributeError.", body_style)
        ]
    ]
    bugs_table = Table(bugs_data, colWidths=[110, 100, 100, 194])
    bugs_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(bugs_table)
    story.append(Spacer(1, 10))

    # Step 5: Defensive Hardening
    story.append(Paragraph("5. Step 5: Defensive Programming & Code Hardening", h1_style))
    story.append(Paragraph(
        "To eliminate all vulnerabilities discovered by fuzz testing, we applied defensive programming techniques: "
        "<br/>1. <b>Type and Null Safety:</b> Explicit validation ensuring inputs are non-null strings (<code>isinstance(text, str)</code>). "
        "<br/>2. <b>Delimiter Validation:</b> Strict validation verifying that delimiters (<code>:</code>, <code>|</code>) appear exactly once. "
        "<br/>3. <b>Sanitization & Numeric Bounds:</b> Safe parsing of numbers guarding against non-numeric tokens, negative values, and special float literals (<code>math.isnan</code>, <code>math.isinf</code>). "
        "<br/>4. <b>Safe Fallbacks:</b> Returning <code>None</code> on invalid inputs rather than allowing unhandled exceptions to crash the application.",
        body_style
    ))

    # Step 5 Image
    img_h_step5 = img_w * (510 / 1040)
    story.append(Image("step5_run_fixed_processor.png", width=img_w, height=img_h_step5))
    story.append(Paragraph("<b>Figure 3:</b> Step 5 — Execution of hardened application under standard inputs and malformed edge cases.", caption_style))

    story.append(PageBreak())

    # Step 6: Verification & Passing Tests
    story.append(Paragraph("6. Step 6: Fuzz Testing Verification on Hardened Code", h1_style))
    story.append(Paragraph(
        "We re-ran the Hypothesis test suite against the hardened implementation across hundreds of generated edge-case inputs. "
        "All property-based fuzz tests and domain correctness assertions passed with zero crashes and 100% success rate:",
        body_style
    ))

    # Step 6 Image
    img_h_step6 = img_w * (643 / 1040)
    story.append(Image("step6_pytest_fixed_passes.png", width=img_w, height=img_h_step6))
    story.append(Paragraph("<b>Figure 4:</b> Step 6 — Pytest Hypothesis test suite achieving 100% pass on hardened implementation.", caption_style))

    # Conclusion
    story.append(Paragraph("7. Conclusion & Key Takeaways", h1_style))
    story.append(Paragraph(
        "1. <b>Fuzzing as a Quality Assurance Tool:</b> Hypothesis successfully identified edge cases that manual unit tests would rarely cover, "
        "including null values, empty strings, delimiter mismatches, and invalid literal conversions.<br/>"
        "2. <b>Defensive Programming:</b> Validating boundaries and sanitizing inputs at the perimeter prevents unhandled crashes and protects downstream services.<br/>"
        "3. <b>All Deliverables Satisfied:</b> Hardened code (<code>scholarship_awards.py</code> / <code>processor.py</code>), test suites (<code>test_scholarship_awards.py</code> / <code>test_processor.py</code>), terminal screenshots, and report are fully compiled.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF: {pdf_path}")

if __name__ == "__main__":
    create_report()
