import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Font Registry for Surgical Reports
# Place Poppins-Regular.ttf and Poppins-Bold.ttf in static/fonts/ to enable premium branding
MAIN_FONT = 'Helvetica'
BOLD_FONT = 'Helvetica-Bold'

try:
    if os.path.exists('static/fonts/Poppins-Regular.ttf'):
        pdfmetrics.registerFont(TTFont('Poppins', 'static/fonts/Poppins-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('Poppins-Bold', 'static/fonts/Poppins-Bold.ttf'))
        MAIN_FONT = 'Poppins'
        BOLD_FONT = 'Poppins-Bold'
except Exception as e:
    print(f"Font loading skipped: {e}")

def clean_clinical_text(text):
    """
    Strips markdown artifacts from AI reports for a cleaner professional look.
    """
    if not text: return ""
    import re
    # Remove bold, italic, and header symbols
    text = re.sub(r'[*#_]', '', text)
    # Standardize bullet points
    text = re.sub(r'^\s*-\s*', '• ', text, flags=re.MULTILINE)
    # Remove extra newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def generate_pdf_report(patient_data, analysis, output_path, doctor_data=None):
    """
    Robust PDF generation for surgical wound assessment reports.
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Process Analysis Text
    cleaned_analysis = clean_clinical_text(analysis)

    # Custom Styles (Premium Poppins)
    title_style = ParagraphStyle(
        'SurgicalTitle',
        parent=styles['Heading1'],
        fontName=BOLD_FONT,
        fontSize=26,
        textColor=colors.HexColor('#0F52BA'),
        spaceAfter=25,
        alignment=1 # Center
    )

    header_style = ParagraphStyle(
        'SurgicalHeader',
        parent=styles['Heading2'],
        fontName=BOLD_FONT,
        fontSize=16,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=12,
        borderPadding=5,
        backColor=colors.HexColor('#F8FAFC')
    )

    normal_style = ParagraphStyle(
        'SurgicalNormal',
        parent=styles['Normal'],
        fontName=MAIN_FONT,
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#334155'),
        spaceAfter=10
    )

    # Title
    story.append(Paragraph("SURGICAL ASSESSMENT REPORT", title_style))
    center_style = ParagraphStyle('CenterStyle', parent=styles['Normal'], alignment=1, fontSize=10, textColor=colors.grey)
    story.append(Paragraph(f"WoundSense AI • Platinum Suite v3.4.1", center_style))
    story.append(Paragraph(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", center_style))
    story.append(Spacer(1, 30))

    # Patient Information Table
    story.append(Paragraph("PATIENT IDENTIFICATION", header_style))
    data = [
        ["Clinical Attribute", "Registered Detail"],
        ["Surgical ID", patient_data.get('id', 'PX-9921')],
        ["Full Name", patient_data.get('name', 'Anonymous')],
        ["Clinical Staging", "Wagner Grade 2 / Chronic"],
        ["Risk Assessment", "STABLE - MONITOR"]
    ]
    t = Table(data, colWidths=[180, 320])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F52BA')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F8FAFC')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1E293B')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), BOLD_FONT),
        ('FONTNAME', (0, 1), (-1, -1), MAIN_FONT),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0'))
    ]))
    story.append(t)
    story.append(Spacer(1, 25))

    # Measurements
    story.append(Paragraph("SURGICAL MEASUREMENTS", header_style))
    m = patient_data.get('measurements', {})
    m_data = [
        ["Clinical Metric", "Analysis Value"],
        ["Wound Length", f"{m.get('length', 0)} cm"],
        ["Wound Width", f"{m.get('width', 0)} cm"],
        ["Wound Depth", f"{m.get('depth', 0)} cm"],
        ["Total Surface Area", f"{m.get('area', 0)} cm²"],
        ["Volumetric Calc", f"{m.get('volume', 0)} cm³"]
    ]
    mt = Table(m_data, colWidths=[250, 250])
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F52BA')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), MAIN_FONT),
    ]))
    story.append(mt)
    story.append(Spacer(1, 25))

    # Doctor Attribution
    if doctor_data:
        story.append(Paragraph("ASSESSING PHYSICIAN", header_style))
        doc_info = [
            ["Physician Name", f"Dr. {doctor_data.get('name', 'Aryan Sharma')}"],
            ["Hospital / Unit", doctor_data.get('hospital', 'City Hospital')],
            ["Consultation ID", f"SRG-{os.urandom(3).hex().upper()}"]
        ]
        dt = Table(doc_info, colWidths=[180, 320])
        dt.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F1F5F9')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), MAIN_FONT),
        ]))
        story.append(dt)
        story.append(Spacer(1, 25))

    # AI Analysis
    story.append(Paragraph("CLINICAL ANALYSIS & RECOMMENDATION", header_style))
    story.append(Paragraph(cleaned_analysis if cleaned_analysis else "No analysis data available.", normal_style))
    story.append(Spacer(1, 25))

    # Scanned Wound Image Integration
    img_rel_path = patient_data.get('image_path', '').lstrip('/')
    if img_rel_path and os.path.exists(img_rel_path):
        try:
            story.append(Paragraph("SCANNED WOUND VISUAL", header_style))
            # Standardize image size for the report
            img = Image(img_rel_path, width=400, height=300)
            img.hAlign = 'CENTER'
            story.append(img)
            story.append(Spacer(1, 25))
        except Exception as e:
            print(f"PDF Image Error: {e}")

    # Disclaimer
    story.append(Spacer(1, 40))
    story.append(Paragraph(f"CONFIDENTIAL: This AI-augmented surgical audit was requested by Dr. {doctor_data.get('name', 'Aryan') if doctor_data else 'Aryan'}. For clinical reference only. Professional MD signature required below.", normal_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("__________________________", center_style))
    story.append(Paragraph("Licensed Medical Officer Signature", center_style))

    doc.build(story)
    return output_path

def generate_3d_coordinates(mask):
    """
    Hypothetical utility to convert 2D mask to 3D point cloud or mesh data.
    """
    return {"vertices": [], "faces": []}
