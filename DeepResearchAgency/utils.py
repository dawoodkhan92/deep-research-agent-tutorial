"""Utility Functions for Deep Research Workflow"""

import os
import re
from datetime import datetime
from pathlib import Path

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
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
        bottomMargin=18,
    )

    # Get styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor="#2c3e50",
    )

    subtitle_style = ParagraphStyle(
        "CustomSubtitle",
        parent=styles["Heading2"],
        fontSize=12,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor="#7f8c8d",
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leftIndent=0,
        rightIndent=0,
    )

    # Build content
    story = []

    # Title
    story.append(Paragraph("Deep Research Report", title_style))
    story.append(Spacer(1, 12))

    # Query/Subtitle
    story.append(Paragraph(f"Query: {query}", subtitle_style))
    story.append(Spacer(1, 12))

    # Timestamp
    timestamp_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    story.append(Paragraph(timestamp_text, subtitle_style))
    story.append(Spacer(1, 24))

    # Research content
    # Split content into paragraphs and format
    paragraphs = research_content.split("\n\n")
    for para in paragraphs:
        if para.strip():
            # Handle basic markdown-style formatting
            formatted_para = para.strip()

            # Convert **bold** to <b>bold</b>
            formatted_para = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", formatted_para)

            # Convert *italic* to <i>italic</i>
            formatted_para = re.sub(r"\*(.*?)\*", r"<i>\1</i>", formatted_para)

            # Handle headers (lines starting with #)
            if formatted_para.startswith("#"):
                # Count hash symbols
                hash_count = len(formatted_para) - len(formatted_para.lstrip("#"))
                header_text = formatted_para.lstrip("# ").strip()

                if hash_count == 1:
                    header_style = styles["Heading1"]
                elif hash_count == 2:
                    header_style = styles["Heading2"]
                elif hash_count == 3:
                    header_style = styles["Heading3"]
                else:
                    header_style = styles["Heading4"]

                story.append(Spacer(1, 12))
                story.append(Paragraph(header_text, header_style))
                story.append(Spacer(1, 6))
            else:
                story.append(Paragraph(formatted_para, body_style))
                story.append(Spacer(1, 6))

    # Build PDF
    doc.build(story)

    return filepath
