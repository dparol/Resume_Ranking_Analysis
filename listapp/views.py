import re
import spacy
from spacy.matcher import Matcher
from django.shortcuts import render,redirect
from .models import ResumeManager
from PyPDF2 import PdfReader


# Create your views here.

#load ml model to extract (ner) personal informations
nlp = spacy.load('en_core_web_sm')





def index(request):
    return render(request,'index.html')



def upload_resume(request):

    if request.method == 'POST':
        new_resume=request.FILES['resume']
        new_upload=ResumeManager(resume=new_resume)
        new_upload.save()
        resume_path=new_upload.resume.path
        print(resume_path)
        per_info=extract_text_from_pdf(resume_path)
        print('ddddddddddddddddddddddd',per_info.get('candidate_name'))

        # Retrieve the latest ResumeManager instance
        instance_obj = ResumeManager.objects.latest('id')

        # Update the instance with the extracted personal information
        instance_obj.candidate_name = per_info.get('candidate_name')
        instance_obj.candidate_email = per_info.get('candidate_email')
        instance_obj.candidate_contactNumber = per_info.get('candidate_contactNumber')
        instance_obj.candidate_education = per_info.get('candidate_education')
        instance_obj.key_skill = per_info.get('key_skill')

        # Save the changes to the instance
        instance_obj.save()

        
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
            candidate_name=extract_name(text)
            candidate_email=extract_email(text)
            candidate_contactNumber=extract_contact_number_from_resume(text)
            candidate_education=extract_education_from_resume(text)
            key_skill=extract_skills_from_resume(text)
            
            context={
                'candidate_name':candidate_name,
                'candidate_email':candidate_email,
                'candidate_contactNumber':candidate_contactNumber,
                'candidate_education':candidate_education,
                'key_skill':key_skill

            }
        return context
         
    except Exception as e:
        print(f"Error extracting text from PDF {file_path}: {e}")
        return ''


def extract_email(text):
    # Extract Email
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    emails = email_pattern.findall(text)
    email = emails[0] if emails else None  # Assume the first email found is the main email
    return {'email': email}





def extract_name(resume_text):
    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)

    # Define name patterns
    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name and Last name
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name, Middle name, and Last name
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]  # First name, Middle name, Middle name, and Last name
        # Add more patterns as needed
    ]

    for pattern in patterns:
        matcher.add('NAME', patterns=[pattern])

    doc = nlp(resume_text)
    matches = matcher(doc)

    for match_id, start, end in matches:
        span = doc[start:end]
        print(span.text)
        return span.text
    
#function using to extract data in given text
# def extract_name(text):
#     try:
#         doc = nlp(text)
#         # Assume the first PERSON entity found is the name
#         for ent in doc.ents:
#             if ent.label_ == 'PERSON':
#                 print(ent.text)
#                 return ent.text
#         return None
#     except Exception as e:
#         print(f"Error extracting name: {e}")
#         return None
    
def extract_education_from_resume(text):
    education = []

    # List of education keywords to match against
    education_keywords = [
    'BSc', 'B.Sc', 'B.Sc.', 'Bachelors of Science', 'Bachelor of Science',
    'MSc', 'M.Sc', 'M.Sc.', 'Masters of Science', 'Master of Science',
    'PhD', 'Ph.D', 'Doctor of Philosophy',
    'BA', 'B.A', 'B.A.', 'Bachelors of Arts', 'Bachelor of Arts',
    'MA', 'M.A', 'M.A.', 'Masters of Arts', 'Master of Arts',
    'BCom', 'B.Com', 'B.Com.', 'Bachelors of Commerce', 'Bachelor of Commerce',
    'MCom', 'M.Com', 'M.Com.', 'Masters of Commerce', 'Master of Commerce',
    'BE', 'B.E', 'B.E.', 'Bachelor of Engineering',
    'ME', 'M.E', 'M.E.', 'Masters of Engineering', 'Master of Engineering',
    'BTech', 'B.Tech', 'B.Tech.', 'Bachelor of Technology',
    'MTech', 'M.Tech', 'M.Tech.', 'Masters of Technology', 'Master of Technology',
    'BBA', 'B.B.A', 'B.B.A.', 'Bachelor of Business Administration',
    'MBA', 'M.B.A', 'M.B.A.', 'Masters of Business Administration', 'Master of Business Administration',
    'BCom', 'B.Com', 'B.Com.', 'Bachelor of Commerce',
    'MCom', 'M.Com', 'M.Com.', 'Masters of Commerce', 'Master of Commerce',
    'BCA', 'B.C.A', 'B.C.A.', 'Bachelor of Computer Applications',
    'MCA', 'M.C.A', 'M.C.A.', 'Masters of Computer Applications', 'Master of Computer Applications',
    'BSW', 'B.S.W', 'B.S.W.', 'Bachelor of Social Work',
    'MSW', 'M.S.W', 'M.S.W.', 'Masters of Social Work', 'Master of Social Work',
    'BBA', 'B.B.A', 'B.B.A.', 'Bachelor of Business Administration',
    'MBA', 'M.B.A', 'M.B.A.', 'Masters of Business Administration', 'Master of Business Administration',
    'BEd', 'B.Ed', 'B.Ed.', 'Bachelor of Education',
    'MEd', 'M.Ed', 'M.Ed.', 'Masters of Education', 'Master of Education',
    'MBBS', 'M.B.B.S', 'M.B.B.S.', 'Bachelor of Medicine, Bachelor of Surgery',
    'MD', 'M.D', 'M.D.', 'Doctor of Medicine',
    'MS', 'M.S', 'M.S.', 'Master of Surgery',
    'BDS', 'B.D.S', 'B.D.S.', 'Bachelor of Dental Surgery',
    'MDS', 'M.D.S', 'M.D.S.', 'Master of Dental Surgery',
    'LLB', 'L.L.B', 'L.L.B.', 'Bachelor of Laws',
    'LLM', 'L.L.M', 'L.L.M.', 'Master of Laws',
    'BPharm', 'B.Pharm', 'B.Pharm.', 'Bachelor of Pharmacy',
    'MPharm', 'M.Pharm', 'M.Pharm.', 'Master of Pharmacy',
    'PharmD', 'Pharm.D', 'Pharm.D.', 'Doctor of Pharmacy',
    'BArch', 'B.Arch', 'B.Arch.', 'Bachelor of Architecture',
    'MArch', 'M.Arch', 'M.Arch.', 'Master of Architecture',
    'BCS', 'B.C.S', 'B.C.S.', 'Bachelor of Computer Science',
    'MCS', 'M.C.S', 'M.C.S.', 'Masters of Computer Science', 'Master of Computer Science',
    'BFA', 'B.F.A', 'B.F.A.', 'Bachelor of Fine Arts',
    'MFA', 'M.F.A', 'M.F.A.', 'Masters of Fine Arts', 'Master of Fine Arts',
    'BDes', 'B.Des', 'B.Des.', 'Bachelor of Design',
    'MDes', 'M.Des', 'M.Des.', 'Masters of Design', 'Master of Design',
    'BT', 'B.T', 'B.T.', 'Bachelor of Technology',
    'MT', 'M.T', 'M.T.', 'Masters of Technology', 'Master of Technology',
    'BVSc', 'B.V.Sc', 'B.V.Sc.', 'Bachelor of Veterinary Science',
    'MVSc', 'M.V.Sc', 'M.V.Sc.', 'Masters of Veterinary Science', 'Master of Veterinary Science',
    'BLIS', 'B.L.I.S', 'B.L.I.S.', 'Bachelor of Library and Information Science',
    'MLIS', 'M.L.I.S', 'M.L.I.S.', 'Masters of Library and Information Science', 'Master of Library and Information Science',
    'BHM', 'B.H.M', 'B.H.M.', 'Bachelor of Hotel Management',
    'MHM', 'M.H.M', 'M.H.M.', 'Masters of Hotel Management', 'Master of Hotel Management',
    'BMM', 'B.M.M', 'B.M.M.', 'Bachelor of Mass Media',
    'MMM', 'M.M.M', 'M.M.M.', 'Masters of Mass Media', 'Master of Mass Media',
    'BNYS', 'B.N.Y.S', 'B.N.Y.S.', 'Bachelor of Naturopathy and Yogic Sciences',
    'MNYS', 'M.N.Y.S', 'M.N.Y.S.', 'Masters of Naturopathy and Yogic Sciences', 'Master of Naturopathy and Yogic Sciences',
    'BPA', 'B.P.A', 'B.P.A.', 'Bachelor of Performing Arts',
    'MPA', 'M.P.A', 'M.P.A.', 'Masters of Performing Arts', 'Master of Performing Arts',
    'BFA', 'B.F.A', 'B.F.A.', 'Bachelor of Fine Arts',
    'MFA', 'M.F.A', 'M.F.A.', 'Masters of Fine Arts', 'Master of Fine Arts',
    'BPT', 'B.P.T', 'B.P.T.', 'Bachelor of Physiotherapy',
    'MPT', 'M.P.T', 'M.P.T.', 'Masters of Physiotherapy', 'Master of Physiotherapy',
    'BAMS', 'B.A.M.S', 'B.A.M.S.', 'Bachelor of Ayurvedic Medicine and Surgery',
    'BUMS', 'B.U.M.S', 'B.U.M.S.', 'Bachelor of Unani Medicine and Surgery',
    'BHMS', 'B.H.M.S', 'B.H.M.S.', 'Bachelor of Homoeopathic Medicine and Surgery',
    'BASLP', 'B.A.S.L.P', 'B.A.S.L.P.', 'Bachelor of Audiology and Speech-Language Pathology',
    'MASLP', 'M.A.S.L.P', 'M.A.S.L.P.', 'Masters of Audiology and Speech-Language Pathology', 'Master of Audiology and Speech-Language Pathology',
    'BMLT', 'B.M.L.T', 'B.M.L.T.', 'Bachelor of Medical Laboratory Technology',
    'BDS', 'B.D.S', 'B.D.S.', 'Bachelor of Dental Surgery',
    'B.Pharm', 'B.Pharm.', 'Bachelor of Pharmacy',
    'M.Pharm', 'M.Pharm.', 'Master of Pharmacy',
    'B.V.Sc', 'B.V.Sc.', 'Bachelor of Veterinary Science',
    'M.V.Sc', 'M.V.Sc.', 'Master of Veterinary Science',
    'B.A.M.S', 'B.A.M.S.', 'Bachelor of Ayurveda, Medicine, and Surgery',
    'B.H.M.S', 'B.H.M.S.', 'Bachelor of Homeopathic Medicine and Surgery',
    'B.U.M.S', 'B.U.M.S.', 'Bachelor of Unani Medicine and Surgery',
    'B.A.S.L.P', 'B.A.S.L.P.', 'Bachelor of Audiology and Speech-Language Pathology',
    'B.M.L.T', 'B.M.L.T.', 'Bachelor of Medical Laboratory Technology',
    'B.O.T', 'B.O.T.', 'Bachelor of Occupational Therapy',
    'B.P.T', 'B.P.T.', 'Bachelor of Physiotherapy',
    'B.S', 'B.S.', 'Bachelor of Science',
    'M.S', 'M.S.', 'Master of Science',
    'B.E', 'B.E.', 'Bachelor of Engineering',
    'M.E', 'M.E.', 'Master of Engineering',
    'B.Tech', 'B.Tech.', 'Bachelor of Technology',
    'M.Tech', 'M.Tech.', 'Master of Technology',
    'B.Arch', 'B.Arch.', 'Bachelor of Architecture',
    'M.Arch', 'M.Arch.', 'Master of Architecture',
    'B.Des', 'B.Des.', 'Bachelor of Design',
    'M.Des', 'M.Des.', 'Master of Design',
    'BCA', 'BCA.', 'Bachelor of Computer Applications',
    'MCA', 'MCA.', 'Master of Computer Applications',
    'BBA', 'BBA.', 'Bachelor of Business Administration',
    'MBA', 'MBA.', 'Master of Business Administration',
    'BFA', 'BFA.', 'Bachelor of Fine Arts',
    'MFA', 'MFA.', 'Master of Fine Arts',
    'BPA', 'BPA.', 'Bachelor of Performing Arts',
    'MPA', 'MPA.', 'Master of Performing Arts',
    'BHM', 'BHM.', 'Bachelor of Hotel Management',
    'MHM', 'MHM.', 'Master of Hotel Management',
    'BMM', 'BMM.', 'Bachelor of Mass Media',
    'MMM', 'MMM.', 'Master of Mass Media',
    'BMS', 'BMS.', 'Bachelor of Management Studies',
    'MMS', 'MMS.', 'Master of Management Studies',
    'BEMS', 'BEMS.', 'Bachelor of Event Management Studies',
    'MEMS', 'MEMS.', 'Master of Event Management Studies',
    'BEMS', 'BEMS.', 'Bachelor of Environmental Management Studies',
    'MEMS', 'MEMS.', 'Master of Environmental Management Studies',
    'BHMCT', 'BHMCT.', 'Bachelor of Hotel Management and Catering Technology',
    'MHMCT', 'MHMCT.', 'Master of Hotel Management and Catering Technology',
    'BCT', 'BCT.', 'Bachelor of Catering Technology',
    'MCT', 'MCT.', 'Master of Catering Technology',
    'BCFT', 'BCFT.', 'Bachelor of Food Technology',
    'MCFT', 'MCFT.', 'Master of Food Technology',
    'BTTM', 'BTTM.', 'Bachelor of Travel and Tourism Management',
    'MTTM', 'MTTM.', 'Master of Travel and Tourism Management',
    'BHMTT', 'BHMTT.', 'Bachelor of Hotel Management and Travel Technology',
    'MHMTT', 'MHMTT.', 'Master of Hotel Management and Travel Technology',
    'BAM', 'BAM.', 'Bachelor of Applied Mathematics',
    'MAM', 'MAM.', 'Master of Applied Mathematics',
    'BAMS', 'BAMS.', 'Bachelor of Ayurvedic Medicine and Surgery',
    'MAMS', 'MAMS.', 'Master of Ayurvedic Medicine and Surgery',
    'BBAE', 'BBAE.', 'Bachelor of Business Administration and Economics',
    'MBAE', 'MBAE.', 'Master of Business Administration and Economics',
    'BBM', 'BBM.', 'Bachelor of Business Management',
    'MBM', 'MBM.', 'Master of Business Management',
    'BBS', 'BBS.', 'Bachelor of Business Studies',
    'MBS', 'MBS.', 'Master of Business Studies',
    'BComm', 'BComm.', 'Bachelor of Commerce',
    'MComm', 'MComm.', 'Master of Commerce']


    for keyword in education_keywords:
        pattern = r"(?i)\b{}\b".format(re.escape(keyword))
        match = re.search(pattern, text)
        if match:
            education.append(match.group())

    return education


def extract_skills_from_resume(text):
    skills = []
    skills_list = [
        "Python", "Java", "C++", "JavaScript", "HTML", "CSS", "SQL", "R", "Swift", "Kotlin",
        "Machine Learning", "Deep Learning", "Data Science", "Data Analysis", "Data Visualization",
        "Natural Language Processing", "Computer Vision", "Artificial Intelligence", "Neural Networks",
        "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn",
        "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "Ruby on Rails",
        "Git", "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud", "Heroku",
        "Agile", "Scrum", "Kanban", "DevOps", "CI/CD", "Testing", "Debugging",
        "Linux", "Unix", "Windows", "MacOS", "Shell Scripting", "Bash", "PowerShell",
        "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Firebase", "Redis", "Elasticsearch",
        "RESTful API", "GraphQL", "SOAP", "Swagger", "OAuth", "JWT", "OAuth2",
        "HTML5", "CSS3", "Responsive Design", "SASS", "LESS", "Bootstrap", "Tailwind CSS",
        "jQuery", "D3.js", "Plotly", "Highcharts", "Tableau", "Google Analytics", "Adobe Analytics",
        "UI/UX Design", "Wireframing", "Prototyping", "Adobe XD", "Figma", "Sketch",
        "Photoshop", "Illustrator", "InDesign", "Premiere Pro", "After Effects", "Final Cut Pro",
        "Microsoft Office", "Google Workspace", "Slack", "Microsoft Teams", "Zoom", "Trello",
        "Jira", "Asana", "Confluence", "Notion", "GitHub", "Bitbucket", "GitLab",
        "TDD", "BDD", "SOLID Principles", "Design Patterns", "Refactoring", "Code Review",
        "Technical Documentation", "API Documentation", "User Stories", "Use Cases", "Requirements Gathering",
        "Project Management", "Agile Project Management", "Waterfall Project Management", "Kanban Project Management", "Scrum Project Management"
    ]

    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)

    return skills


def extract_contact_number_from_resume(text):
    contact_number = None

    # Use regex pattern to find a potential contact number
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()

    return contact_number