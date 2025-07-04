"""Utility Functions for Deep Research Workflow"""

import os
import re
from datetime import datetime
from pathlib import Path

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def save_research_to_pdf(
    research_content: str,
    query: str = "Research Report",
    output_dir: str = "reports",
    filename: str = None,
) -> str:
    """
    Save research content to a professionally formatted PDF.

    Args:
        research_content: The research text to save
        query: Original research query for the title
        output_dir: Directory to save the PDF (default: 'reports')
        filename: Custom filename (optional, auto-generated if not provided)

    Returns:
        str: Path to the saved PDF file
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)

    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_query = "".join(
            c for c in query[:50] if c.isalnum() or c in (" ", "-", "_")
        ).strip()
        safe_query = safe_query.replace(" ", "_")
        filename = f"research_report_{safe_query}_{timestamp}.pdf"

    # Ensure .pdf extension
    if not filename.endswith(".pdf"):
        filename += ".pdf"

    filepath = os.path.join(output_dir, filename)

    # Create PDF document
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
    )

    # Get styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=20,
        spaceAfter=0.3 * inch,
        alignment=TA_CENTER,
        textColor="#2c3e50",
    )

    subtitle_style = ParagraphStyle(
        "CustomSubtitle",
        parent=styles["Heading2"],
        fontSize=12,
        spaceAfter=0.2 * inch,
        alignment=TA_CENTER,
        textColor="#7f8c8d",
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=11,
        spaceAfter=0.15 * inch,
        alignment=TA_JUSTIFY,
        leftIndent=0,
        rightIndent=0,
        leading=14,  # Line spacing
    )

    # Custom header styles
    header1_style = ParagraphStyle(
        "CustomHeader1",
        parent=styles["Heading1"],
        fontSize=16,
        spaceAfter=0.2 * inch,
        spaceBefore=0.3 * inch,
        alignment=TA_LEFT,
        textColor="#2c3e50",
    )

    header2_style = ParagraphStyle(
        "CustomHeader2",
        parent=styles["Heading2"],
        fontSize=14,
        spaceAfter=0.15 * inch,
        spaceBefore=0.2 * inch,
        alignment=TA_LEFT,
        textColor="#34495e",
    )

    header3_style = ParagraphStyle(
        "CustomHeader3",
        parent=styles["Heading3"],
        fontSize=12,
        spaceAfter=0.1 * inch,
        spaceBefore=0.15 * inch,
        alignment=TA_LEFT,
        textColor="#34495e",
    )

    # List item style
    list_style = ParagraphStyle(
        "CustomList",
        parent=styles["Normal"],
        fontSize=11,
        spaceAfter=0.05 * inch,
        leftIndent=0.25 * inch,
        bulletIndent=0.1 * inch,
        alignment=TA_LEFT,
        leading=14,
    )

    # Build content
    story = []

    # Title
    story.append(Paragraph("Deep Research Report", title_style))
    story.append(Spacer(1, 0.1 * inch))

    # Query/Subtitle
    story.append(Paragraph(f"Query: {_escape_html(query)}", subtitle_style))
    story.append(Spacer(1, 0.1 * inch))

    # Timestamp
    timestamp_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    story.append(Paragraph(timestamp_text, subtitle_style))
    story.append(Spacer(1, 0.3 * inch))

    # Process research content
    lines = research_content.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            # Skip empty lines but add small spacer
            story.append(Spacer(1, 0.05 * inch))
            i += 1
            continue

        # Handle headers
        if line.startswith("#"):
            hash_count = len(line) - len(line.lstrip("#"))
            header_text = line.lstrip("# ").strip()

            if hash_count == 1:
                story.append(Paragraph(_escape_html(header_text), header1_style))
            elif hash_count == 2:
                story.append(Paragraph(_escape_html(header_text), header2_style))
            else:
                story.append(Paragraph(_escape_html(header_text), header3_style))

        # Handle list items
        elif line.startswith(("- ", "* ", "• ")):
            bullet_text = line[2:].strip()
            story.append(Paragraph(f"• {_format_inline_text(bullet_text)}", list_style))

        # Handle numbered lists
        elif re.match(r"^\d+\.\s+", line):
            story.append(Paragraph(_format_inline_text(line), list_style))

        # Handle regular paragraphs
        else:
            # Collect continuation lines for multi-line paragraphs
            paragraph_lines = [line]
            j = i + 1
            while (
                j < len(lines)
                and lines[j].strip()
                and not lines[j].startswith("#")
                and not lines[j].startswith(("- ", "* ", "• "))
                and not re.match(r"^\d+\.\s+", lines[j])
            ):
                paragraph_lines.append(lines[j].strip())
                j += 1

            # Join paragraph lines
            paragraph_text = " ".join(paragraph_lines)
            story.append(Paragraph(_format_inline_text(paragraph_text), body_style))

            # Skip the lines we've processed
            i = j - 1

        i += 1

    # Build PDF
    doc.build(story)

    return filepath


def _escape_html(text: str) -> str:
    """Escape HTML special characters for ReportLab."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _format_inline_text(text: str) -> str:
    """Format inline text with bold, italic, and HTML escaping."""
    # First escape HTML
    text = _escape_html(text)

    # Convert **bold** to <b>bold</b>
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

    # Convert *italic* to <i>italic</i> (but not if it's part of **bold**)
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", text)

    # Convert `code` to monospace
    text = re.sub(r"`([^`]+?)`", r'<font name="Courier">\1</font>', text)

    return text
