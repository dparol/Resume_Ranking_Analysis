import re
from django.shortcuts import render,redirect
from .models import ResumeManager
from PyPDF2 import PdfReader

# Create your views here.
def index(request):
    return render(request,'index.html')

def upload_resume(request):
    if request.method == 'POST':
        new_resume=request.FILES['resume']
        new_upload=ResumeManager(resume=new_resume)
        new_upload.save()
        resume_path=new_upload.resume.path
        print(resume_path)
        data=extract_text_from_pdf(resume_path)
    return redirect('index')


def extract_text_from_pdf(file_path):
    try:
        print('enter the function')
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            number_of_pages = len(reader.pages)
            print(number_of_pages)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            personal_info=extract_information(text)
            print(personal_info)
            return text
    except Exception as e:
        print(f"Error extracting text from PDF {file_path}: {e}")
        return ''


def extract_information(text):
    # Extract Name
    name_pattern = re.compile(r'\b[A-Z]+\b')  # Simple pattern for name
    names = name_pattern.findall(text)
    name = ' '.join(names)  # Concatenate multiple names if found

    # Extract Email
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    emails = email_pattern.findall(text)
    email = emails[0] if emails else None  # Assume the first email found is the main email

    # Extract Skills (example skills list)
    skills = ['Python', 'Java', 'JavaScript', 'SQL', 'Machine Learning', 'Data Analysis']
    skill_matches = [skill for skill in skills if re.search(r'\b{}\b'.format(skill), text, re.IGNORECASE)]

    return {'name': name, 'email': email, 'skills': skill_matches}


