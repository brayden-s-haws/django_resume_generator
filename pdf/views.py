from django.shortcuts import render
from .models import Profile
from django.http import HttpResponse
from django.template import loader
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from io import BytesIO

# Create your views here.
def accept(request):

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        about = request.POST.get('about', '')
        degree = request.POST.get('degree', '')
        school = request.POST.get('school', '')
        university = request.POST.get('university', '')
        previous_work = request.POST.get('previous_work', '')
        skills = request.POST.get('skills', '')

        profile = Profile.objects.create(name=name, email=email, phone=phone, about=about, degree=degree, school=school, university=university, previous_work=previous_work, skills=skills)
        profile.save()


    return render(request, 'pdf/accept.html')

def resume(request, id):
    user_profile = Profile.objects.get(pk=id)
    
    # Create a BytesIO buffer for the PDF
    buffer = BytesIO()
    
    # Create the PDF object using ReportLab
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#2C3E50',
        spaceAfter=12,
        alignment=1  # Center alignment
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor='#34495E',
        spaceAfter=6,
        spaceBefore=12
    )
    normal_style = styles['Normal']
    
    # Add content to PDF
    story.append(Paragraph(user_profile.name, title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Contact Information
    contact_text = f"Email: {user_profile.email} | Phone: {user_profile.phone}"
    story.append(Paragraph(contact_text, normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(HRFlowable(width="100%", thickness=1, color='#CCCCCC', spaceBefore=0, spaceAfter=0.2*inch))
    
    # About Section
    if user_profile.about:
        story.append(Paragraph("About", heading_style))
        story.append(Paragraph(user_profile.about, normal_style))
        story.append(Spacer(1, 0.1*inch))
        story.append(HRFlowable(width="100%", thickness=1, color='#CCCCCC', spaceBefore=0, spaceAfter=0.2*inch))
    
    # Education Section
    if user_profile.degree or user_profile.school or user_profile.university:
        story.append(Paragraph("Education", heading_style))
        if user_profile.degree:
            story.append(Paragraph(f"<b>Degree:</b> {user_profile.degree}", normal_style))
        if user_profile.school:
            story.append(Paragraph(f"<b>School:</b> {user_profile.school}", normal_style))
        if user_profile.university:
            story.append(Paragraph(f"<b>University:</b> {user_profile.university}", normal_style))
        story.append(Spacer(1, 0.1*inch))
        story.append(HRFlowable(width="100%", thickness=1, color='#CCCCCC', spaceBefore=0, spaceAfter=0.2*inch))
    
    # Work Experience Section
    if user_profile.previous_work:
        story.append(Paragraph("Work Experience", heading_style))
        story.append(Paragraph(user_profile.previous_work, normal_style))
        story.append(Spacer(1, 0.1*inch))
        story.append(HRFlowable(width="100%", thickness=1, color='#CCCCCC', spaceBefore=0, spaceAfter=0.2*inch))
    
    # Skills Section
    if user_profile.skills:
        story.append(Paragraph("Skills", heading_style))
        story.append(Paragraph(user_profile.skills, normal_style))
    
    # Build PDF
    doc.build(story)
    
    # Get the PDF value
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{user_profile.name}_resume.pdf"'
    
    return response

def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'pdf/profile_list.html', {'profiles': profiles})