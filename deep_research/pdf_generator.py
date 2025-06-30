"""Top-notch Markdown to PDF Conversion - Reliable Cross-Platform Implementation"""

import re
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

def save_to_pdf(content: str, title: str = "Research Report", output_dir: str = "outputs") -> str:
    """
    One-liner top-notch markdown-to-PDF conversion using reportlab.
    
    Args:
        content: Markdown content to convert
        title: Document title
        output_dir: Output directory
        
    Returns:
        str: Path to generated PDF file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    Path(output_dir).mkdir(exist_ok=True)
    pdf_path = f"{output_dir}/{title.replace(' ', '_')}_{timestamp}.pdf"
    
    # Create PDF document
    doc = SimpleDocTemplate(
        pdf_path, 
        pagesize=letter,
        leftMargin=inch, 
        rightMargin=inch,
        topMargin=inch, 
        bottomMargin=inch
    )
    
    # Get styles and create custom ones
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles for professional appearance
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#2c3e50'),
        fontName='Helvetica-Bold'
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=12,
        textColor=colors.HexColor('#2c3e50'),
        fontName='Helvetica-Bold'
    )
    
    subheader_style = ParagraphStyle(
        'CustomSubHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=16,
        spaceAfter=8,
        textColor=colors.HexColor('#34495e'),
        fontName='Helvetica-Bold'
    )
    
    # Add title and timestamp
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
        styles['Normal']
    ))
    story.append(Spacer(1, 20))
    
    # Process markdown content line by line
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 6))
            continue
            
        # Handle headers
        if line.startswith('### '):
            text = line[4:].strip()
            story.append(Paragraph(text, subheader_style))
        elif line.startswith('## '):
            text = line[3:].strip()
            story.append(Paragraph(text, header_style))
        elif line.startswith('# '):
            text = line[2:].strip()
            story.append(Paragraph(text, header_style))
        
        # Handle bold text
        elif line.startswith('**') and line.endswith('**') and len(line) > 4:
            text = f"<b>{line[2:-2]}</b>"
            story.append(Paragraph(text, styles['Normal']))
            
        # Handle bullet points
        elif line.startswith('- ') or line.startswith('* '):
            text = f"• {line[2:].strip()}"
            story.append(Paragraph(text, styles['Normal']))
            
        # Handle numbered lists
        elif re.match(r'^\d+\.\s', line):
            story.append(Paragraph(line, styles['Normal']))
            
        # Regular paragraphs
        else:
            # Clean up any remaining markdown
            text = line.replace('**', '<b>').replace('**', '</b>')
            text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)  # Italic
            story.append(Paragraph(text, styles['Normal']))
        
        story.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(story)
    
    print(f"✅ PDF generated: {pdf_path}")
    return pdf_path 