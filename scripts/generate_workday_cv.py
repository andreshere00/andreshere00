#!/usr/bin/env python3
"""Generate a Workday-ATS-friendly resume in DOCX and TXT.

The layout is single-column, uses a standard font, avoids tables/text boxes/
headers/footers, and uses section titles Workday commonly maps to profile fields.
"""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Inches, Pt, RGBColor


OUTPUT_DIR = Path(__file__).resolve().parents[1] / "cv"
DOCX_PATH = OUTPUT_DIR / "Andres_Herencia_CV_Workday.docx"
TXT_PATH = OUTPUT_DIR / "Andres_Herencia_CV_Workday.txt"

FONT_NAME = "Calibri"
BODY_SIZE = 11
NAME_SIZE = 22
TITLE_SIZE = 12
SECTION_SIZE = 13
MUTED = RGBColor(0x33, 0x33, 0x33)
BLACK = RGBColor(0x00, 0x00, 0x00)


def set_run_font(run, size_pt: int, bold: bool = False, color: RGBColor = BLACK) -> None:
    """Apply Calibri and size to a run, including East-Asian fallback."""
    run.bold = bold
    run.font.size = Pt(size_pt)
    run.font.color.rgb = color
    run.font.name = FONT_NAME
    r_pr = run._element.get_or_add_rPr()
    r_fonts = r_pr.find(qn("w:rFonts"))
    if r_fonts is None:
        r_fonts = OxmlElement("w:rFonts")
        r_pr.append(r_fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        r_fonts.set(qn(attr), FONT_NAME)


def set_paragraph_spacing(
    paragraph,
    before_pt: float = 0,
    after_pt: float = 0,
    line_pt: float = 14,
) -> None:
    """Tighten paragraph spacing for a compact one-page-friendly resume."""
    pf = paragraph.paragraph_format
    pf.space_before = Pt(before_pt)
    pf.space_after = Pt(after_pt)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(line_pt)
    pf.widow_control = True


def add_bottom_border(paragraph) -> None:
    """Add a simple underline under section headings (still extractable as text)."""
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "12")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "000000")
    p_bdr.append(bottom)
    p_pr.append(p_bdr)


def add_text(
    paragraph,
    text: str,
    size: int = BODY_SIZE,
    bold: bool = False,
    color: RGBColor = BLACK,
) -> None:
    run = paragraph.add_run(text)
    set_run_font(run, size, bold=bold, color=color)


def add_paragraph(document: Document, text: str = "", **kwargs):
    paragraph = document.add_paragraph()
    before = kwargs.pop("before", 0)
    after = kwargs.pop("after", 0)
    line = kwargs.pop("line", 14)
    align = kwargs.pop("align", WD_ALIGN_PARAGRAPH.LEFT)
    size = kwargs.pop("size", BODY_SIZE)
    bold = kwargs.pop("bold", False)
    color = kwargs.pop("color", BLACK)
    set_paragraph_spacing(paragraph, before, after, line)
    paragraph.alignment = align
    if text:
        add_text(paragraph, text, size=size, bold=bold, color=color)
    return paragraph


def add_section(document: Document, title: str) -> None:
    paragraph = add_paragraph(
        document,
        title.upper(),
        before=10,
        after=4,
        line=16,
        size=SECTION_SIZE,
        bold=True,
    )
    add_bottom_border(paragraph)


def add_job_header(
    document: Document,
    title: str,
    employer: str,
    location: str,
    dates: str,
) -> None:
    """Write a Workday-friendly job block: title, employer, location, dates."""
    add_paragraph(document, title, before=8, after=0, line=15, size=12, bold=True)
    add_paragraph(
        document,
        f"{employer} | {location}",
        before=0,
        after=0,
        line=14,
        size=11,
        bold=False,
        color=MUTED,
    )
    add_paragraph(document, dates, before=0, after=2, line=14, size=10, color=MUTED)


def add_bullet(document: Document, text: str) -> None:
    paragraph = document.add_paragraph(style="List Bullet")
    set_paragraph_spacing(paragraph, before_pt=0, after_pt=1, line_pt=14)
    paragraph.clear()
    add_text(paragraph, text, size=BODY_SIZE)
    # Keep bullets close to the left margin for parser stability.
    paragraph.paragraph_format.left_indent = Inches(0.25)
    paragraph.paragraph_format.first_line_indent = Inches(-0.15)


def configure_document(document: Document) -> None:
    section = document.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)
    section.header_distance = Inches(0.3)
    section.footer_distance = Inches(0.3)

    styles = document.styles
    normal = styles["Normal"]
    normal.font.name = FONT_NAME
    normal.font.size = Pt(BODY_SIZE)
    normal.font.color.rgb = BLACK
    r_pr = normal.element.get_or_add_rPr()
    r_fonts = r_pr.find(qn("w:rFonts"))
    if r_fonts is None:
        r_fonts = OxmlElement("w:rFonts")
        r_pr.append(r_fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        r_fonts.set(qn(attr), FONT_NAME)

    pf = normal.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)

    # Do not put contact data in header/footer: Workday often ignores them.


def build_docx() -> Document:
    document = Document()
    configure_document(document)

    add_paragraph(
        document,
        "Andrés Herencia",
        before=0,
        after=2,
        line=26,
        size=NAME_SIZE,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
    )

    add_paragraph(
        document,
        "Forward Deployed AI Engineer | 2x AWS Certified | 3+ years designing and building AI-driven products",
        before=0,
        after=6,
        line=15,
        size=TITLE_SIZE,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
    )

    contact = add_paragraph(document, align=WD_ALIGN_PARAGRAPH.CENTER, after=2, line=14)
    add_text(contact, "Madrid, Spain  |  +34 608 325 729  |  ")
    add_text(contact, "andresherencia2000@gmail.com")
    contact2 = add_paragraph(document, align=WD_ALIGN_PARAGRAPH.CENTER, after=4, line=14)
    add_text(contact2, "LinkedIn: https://www.linkedin.com/in/andres-herencia/  |  ")
    add_text(contact2, "GitHub: https://github.com/andreshere00")

    add_section(document, "Professional Summary")
    add_paragraph(
        document,
        (
            "Forward Deployed AI Engineer with 3+ years of experience designing and building "
            "AI-driven products using large language models (LLMs), retrieval-augmented generation "
            "(RAG), agentic tools, and Amazon Web Services (AWS). Track record delivering "
            "production systems in banking, credit risk, mobility, and consulting."
        ),
        before=2,
        after=2,
        line=14,
    )

    add_section(document, "Work Experience")

    add_job_header(
        document,
        "Forward Deployed AI Engineer",
        "InnoIT (client: one of the Big Three credit risk agencies)",
        "Madrid, Spain",
        "February 2026 - Present",
    )
    add_bullet(
        document,
        "Design and build agentic tools in TypeScript using skills and Model Context Protocol (MCP) servers.",
    )
    add_bullet(
        document,
        "Developed an event-driven architecture on AWS to generate Early Warning System (EWS) reports, reducing delivery time from 4-5 days to under 10 minutes.",
    )
    add_bullet(
        document,
        "Lead internal use cases for consulting engagements and support role profiling through technical interviews.",
    )

    add_job_header(
        document,
        "Machine Learning Engineer",
        "Minsait, assigned to BBVA",
        "Madrid, Spain",
        "September 2024 - February 2026",
    )
    add_bullet(
        document,
        "Developed a serverless generative AI application to automate claims classification, reaching 98% accuracy and cutting complaint-mail triage from hours to under 3 minutes.",
    )
    add_bullet(
        document,
        "Led planning and delivery for internal Minsait projects: BigRAG (Microsoft Azure) and LLM Evaluator.",
    )

    add_job_header(
        document,
        "DevOps and MLOps Engineer",
        "The Cliff",
        "Madrid, Spain",
        "February 2024 - September 2024",
    )
    add_bullet(
        document,
        "Scaled and automated AWS cloud infrastructure, with CI/CD pipelines to deploy microservices.",
    )
    add_bullet(
        document,
        "Improved LLM performance and observability by delivering MLOps workflows for RAG systems.",
    )

    add_job_header(
        document,
        "Big Data and Data Science Researcher (Part-time)",
        "SUNRISE European Project",
        "Madrid, Spain",
        "December 2021 - April 2023",
    )
    add_bullet(
        document,
        "Built and trained a logistic optimization model for the CRTM transport network.",
    )
    add_bullet(
        document,
        "Performed geospatial data analysis using the Google Earth Engine API and PySpark.",
    )

    add_job_header(
        document,
        "Data Science Intern",
        "Cabify Chair",
        "Madrid, Spain",
        "December 2021 - April 2023",
    )
    add_bullet(
        document,
        "Developed statistical models for a mobility simulation platform actively used by the company.",
    )
    add_bullet(
        document,
        "Presented this work as a Bachelor's Thesis, awarded the maximum grade (10/10).",
    )

    add_section(document, "Education")

    add_paragraph(
        document,
        "Master's Degree in Statistical and Computational Methods for Data Science",
        before=8,
        after=0,
        line=15,
        size=12,
        bold=True,
    )
    add_paragraph(
        document,
        "Universidad Complutense de Madrid and Universidad Politécnica de Madrid | Madrid, Spain",
        before=0,
        after=0,
        line=14,
        color=MUTED,
    )
    add_paragraph(
        document,
        "September 2023 - June 2024  |  Grade: 9/10",
        before=0,
        after=2,
        line=14,
        size=10,
        color=MUTED,
    )
    add_bullet(
        document,
        "Thesis: Analysis of the Transformer architecture and foundation model fine-tuning using QLoRA (Grade: 9.8/10).",
    )

    add_paragraph(
        document,
        "Bachelor's Degree in Telecommunication Engineering",
        before=8,
        after=0,
        line=15,
        size=12,
        bold=True,
    )
    add_paragraph(
        document,
        "Universidad Politécnica de Madrid | Madrid, Spain",
        before=0,
        after=0,
        line=14,
        color=MUTED,
    )
    add_paragraph(
        document,
        "September 2018 - July 2022",
        before=0,
        after=2,
        line=14,
        size=10,
        color=MUTED,
    )

    add_section(document, "Certifications")
    add_paragraph(
        document,
        "AWS Certified Solutions Architect - Associate, Amazon Web Services (AWS)",
        before=6,
        after=0,
        line=14,
        bold=True,
    )
    add_paragraph(
        document,
        "Issued April 2025  |  Expires April 2028  |  https://www.credly.com/badges/6f0a5952-ad44-4b76-b609-ac3ae21466a1/public_url",
        before=0,
        after=4,
        line=13,
        size=10,
        color=MUTED,
    )
    add_paragraph(
        document,
        "AWS Certified Machine Learning Engineer - Associate, Amazon Web Services (AWS)",
        before=2,
        after=0,
        line=14,
        bold=True,
    )
    add_paragraph(
        document,
        "Issued November 2025  |  Expires November 2028  |  https://www.credly.com/badges/94609834-c001-4dec-b8aa-c07957444f1e/public_url",
        before=0,
        after=2,
        line=13,
        size=10,
        color=MUTED,
    )

    add_section(document, "Skills")
    add_paragraph(
        document,
        (
            "Python, TypeScript, Amazon Web Services (AWS), Microsoft Azure, Generative AI, "
            "Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), Agentic AI, "
            "Model Context Protocol (MCP), Event-Driven Architecture, Serverless, MLOps, DevOps, "
            "CI/CD, Microservices, PySpark, Geospatial Analysis, Transformers, QLoRA, Fine-tuning, "
            "Technical Interviews, Consulting"
        ),
        before=4,
        after=2,
        line=14,
    )

    add_section(document, "Projects")
    add_bullet(
        document,
        "SplitterMR: Python library to ingest and transform documents into markdown chunks. GitHub: https://github.com/andreshere00/Splitter_MR/  |  PyPI: https://pypi.org/project/splitter-mr/",
    )
    add_bullet(
        document,
        "GenAI Application template: Cookiecutter template for building LLM-based applications in Python. GitHub: https://github.com/andreshere00/GenAI-app-template",
    )
    add_bullet(
        document,
        "PPTX Generator: End-to-end generative AI MVP that turns natural language prompts and user media into editable PowerPoint decks.",
    )
    add_bullet(
        document,
        "BigRAG: Hybrid search-powered RAG system deployed on Microsoft Azure for large databases.",
    )

    add_section(document, "Languages")
    add_paragraph(
        document,
        "Spanish: Native  |  English: Full professional proficiency  |  Italian: Limited working proficiency",
        before=4,
        after=0,
        line=14,
    )

    return document


def build_txt() -> str:
    """Plain-text twin of the resume for parsers that prefer TXT."""
    return """ANDRÉS HERENCIA
Forward Deployed AI Engineer | 2x AWS Certified | 3+ years designing and building AI-driven products

Madrid, Spain
Phone: +34 608 325 729
Email: andresherencia2000@gmail.com
LinkedIn: https://www.linkedin.com/in/andres-herencia/
GitHub: https://github.com/andreshere00

PROFESSIONAL SUMMARY
Forward Deployed AI Engineer with 3+ years of experience designing and building AI-driven products using large language models (LLMs), retrieval-augmented generation (RAG), agentic tools, and Amazon Web Services (AWS). Track record delivering production systems in banking, credit risk, mobility, and consulting.

WORK EXPERIENCE

Forward Deployed AI Engineer
InnoIT (client: one of the Big Three credit risk agencies)
Madrid, Spain
February 2026 - Present
- Design and build agentic tools in TypeScript using skills and Model Context Protocol (MCP) servers.
- Developed an event-driven architecture on AWS to generate Early Warning System (EWS) reports, reducing delivery time from 4-5 days to under 10 minutes.
- Lead internal use cases for consulting engagements and support role profiling through technical interviews.

Machine Learning Engineer
Minsait, assigned to BBVA
Madrid, Spain
September 2024 - February 2026
- Developed a serverless generative AI application to automate claims classification, reaching 98% accuracy and cutting complaint-mail triage from hours to under 3 minutes.
- Led planning and delivery for internal Minsait projects: BigRAG (Microsoft Azure) and LLM Evaluator.

DevOps and MLOps Engineer
The Cliff
Madrid, Spain
February 2024 - September 2024
- Scaled and automated AWS cloud infrastructure, with CI/CD pipelines to deploy microservices.
- Improved LLM performance and observability by delivering MLOps workflows for RAG systems.

Big Data and Data Science Researcher (Part-time)
SUNRISE European Project
Madrid, Spain
December 2021 - April 2023
- Built and trained a logistic optimization model for the CRTM transport network.
- Performed geospatial data analysis using the Google Earth Engine API and PySpark.

Data Science Intern
Cabify Chair
Madrid, Spain
December 2021 - April 2023
- Developed statistical models for a mobility simulation platform actively used by the company.
- Presented this work as a Bachelor's Thesis, awarded the maximum grade (10/10).

EDUCATION

Master's Degree in Statistical and Computational Methods for Data Science
Universidad Complutense de Madrid and Universidad Politécnica de Madrid
Madrid, Spain
September 2023 - June 2024
Grade: 9/10
- Thesis: Analysis of the Transformer architecture and foundation model fine-tuning using QLoRA (Grade: 9.8/10).

Bachelor's Degree in Telecommunication Engineering
Universidad Politécnica de Madrid
Madrid, Spain
September 2018 - July 2022

CERTIFICATIONS

AWS Certified Solutions Architect - Associate, Amazon Web Services (AWS)
Issued April 2025 | Expires April 2028
https://www.credly.com/badges/6f0a5952-ad44-4b76-b609-ac3ae21466a1/public_url

AWS Certified Machine Learning Engineer - Associate, Amazon Web Services (AWS)
Issued November 2025 | Expires November 2028
https://www.credly.com/badges/94609834-c001-4dec-b8aa-c07957444f1e/public_url

SKILLS
Python, TypeScript, Amazon Web Services (AWS), Microsoft Azure, Generative AI, Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), Agentic AI, Model Context Protocol (MCP), Event-Driven Architecture, Serverless, MLOps, DevOps, CI/CD, Microservices, PySpark, Geospatial Analysis, Transformers, QLoRA, Fine-tuning, Technical Interviews, Consulting

PROJECTS
- SplitterMR: Python library to ingest and transform documents into markdown chunks. GitHub: https://github.com/andreshere00/Splitter_MR/  |  PyPI: https://pypi.org/project/splitter-mr/
- GenAI Application template: Cookiecutter template for building LLM-based applications in Python. GitHub: https://github.com/andreshere00/GenAI-app-template
- PPTX Generator: End-to-end generative AI MVP that turns natural language prompts and user media into editable PowerPoint decks.
- BigRAG: Hybrid search-powered RAG system deployed on Microsoft Azure for large databases.

LANGUAGES
Spanish: Native | English: Full professional proficiency | Italian: Limited working proficiency
"""


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    document = build_docx()
    document.save(DOCX_PATH)
    TXT_PATH.write_text(build_txt(), encoding="utf-8")
    print(f"Wrote {DOCX_PATH}")
    print(f"Wrote {TXT_PATH}")


if __name__ == "__main__":
    main()
