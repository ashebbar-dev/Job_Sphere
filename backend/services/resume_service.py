import openai
import os
import json
import PyPDF2
from io import BytesIO

def extract_resume_text(file_path):
    """Extract text from PDF resume"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Resume extraction error: {e}")
        return None

def parse_resume_with_ai(resume_text):
    """Parse resume using AI to extract structured data"""
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f"""Parse this resume and extract information in JSON format:

Resume:
{resume_text}

Extract:
{{
    "name": "Full name",
    "email": "Email address",
    "phone": "Phone number",
    "skills": ["skill1", "skill2", "skill3"],
    "education": [
        {{
            "degree": "Degree name",
            "institution": "College name",
            "year": "Graduation year",
            "cgpa": "CGPA if available"
        }}
    ],
    "experience": [
        {{
            "title": "Job title",
            "company": "Company name",
            "duration": "Duration",
            "description": "Brief description"
        }}
    ],
    "projects": [
        {{
            "name": "Project name",
            "description": "Description",
            "technologies": ["tech1", "tech2"]
        }}
    ],
    "certifications": ["cert1", "cert2"],
    "summary": "Brief professional summary"
}}

Extract only information present in the resume. Use "Not mentioned" for missing fields."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a resume parsing specialist. Extract information accurately from resumes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )

        response_text = response.choices[0].message.content
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        return json.loads(response_text)

    except Exception as e:
        print(f"Resume parsing error: {e}")
        return None

def calculate_match_score(student_resume, job_analysis, company_research):
    """Calculate how well student matches the job"""
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f"""Analyze the fit between this candidate and job:

Candidate Profile:
{json.dumps(student_resume, indent=2)}

Job Requirements:
{json.dumps(job_analysis, indent=2)}

Company Profile:
{json.dumps(company_research, indent=2)}

Provide analysis in JSON:
{{
    "overall_match_score": 85,
    "skills_match": {{
        "matching_skills": ["skill1", "skill2"],
        "missing_skills": ["skill3", "skill4"],
        "score": 80
    }},
    "experience_fit": {{
        "assessment": "Good fit / Underqualified / Overqualified",
        "score": 75
    }},
    "cultural_fit": {{
        "assessment": "Analysis of cultural alignment",
        "score": 90
    }},
    "strengths": ["strength1", "strength2"],
    "improvement_areas": ["area1", "area2"],
    "recommendation": "Strong recommendation / Consider with reservations / Not recommended"
}}

Score should be 0-100."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a career counselor analyzing candidate-job fit for college placements."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.5
        )

        response_text = response.choices[0].message.content
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        return json.loads(response_text)

    except Exception as e:
        print(f"Match calculation error: {e}")
        return None

def calculate_ats_score(resume_text, job_keywords):
    """Calculate ATS (Applicant Tracking System) compatibility score"""
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f"""Analyze this resume for ATS (Applicant Tracking System) compatibility:

Resume:
{resume_text}

Target Keywords:
{json.dumps(job_keywords, indent=2)}

Provide ATS analysis in JSON:
{{
    "ats_score": 85,
    "keyword_match_percentage": 75,
    "matched_keywords": ["keyword1", "keyword2"],
    "missing_keywords": ["keyword3", "keyword4"],
    "formatting_issues": ["issue1", "issue2"],
    "suggestions": [
        "Add more keywords from job description",
        "Use standard section headings",
        "Avoid tables and complex formatting"
    ],
    "overall_assessment": "Good / Fair / Poor"
}}

Score should be 0-100."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an ATS (Applicant Tracking System) analyzer helping candidates optimize their resumes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.3
        )

        response_text = response.choices[0].message.content
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        return json.loads(response_text)

    except Exception as e:
        print(f"ATS scoring error: {e}")
        return None

def personalize_resume(student_resume, job_analysis, company_research, match_analysis):
    """Generate personalized resume content"""
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f"""Create a personalized resume for this job application:

Original Resume Data:
{json.dumps(student_resume, indent=2)}

Job Requirements:
{json.dumps(job_analysis, indent=2)}

Company Profile:
{json.dumps(company_research, indent=2)}

Match Analysis:
{json.dumps(match_analysis, indent=2)}

Generate personalized content:
{{
    "professional_summary": "Tailored summary highlighting relevant skills and alignment with company",
    "key_highlights": [
        "Highlight 1 emphasizing relevant experience",
        "Highlight 2 showing cultural fit",
        "Highlight 3 addressing key requirement"
    ],
    "skills_section": {{
        "primary_skills": ["Prioritized skills matching job"],
        "secondary_skills": ["Supporting skills"]
    }},
    "personalization_notes": [
        "Changed wording to match company language",
        "Emphasized specific project relevant to role",
        "Reordered skills to prioritize job requirements"
    ]
}}

Focus on authentic personalization, not fabrication."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional resume writer specializing in tailoring resumes for specific job applications."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )

        response_text = response.choices[0].message.content
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        return json.loads(response_text)

    except Exception as e:
        print(f"Resume personalization error: {e}")
        return None

def identify_skills_gap(student_skills, required_skills, preferred_skills):
    """Identify skills gap and provide learning recommendations"""
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f"""Analyze skills gap and provide learning recommendations:

Student's Current Skills:
{json.dumps(student_skills, indent=2)}

Job Required Skills:
{json.dumps(required_skills, indent=2)}

Job Preferred Skills:
{json.dumps(preferred_skills, indent=2)}

Provide analysis:
{{
    "critical_gaps": [
        {{
            "skill": "Skill name",
            "importance": "Critical / Important / Nice-to-have",
            "learning_resources": ["Resource 1", "Resource 2"],
            "estimated_time": "Time to learn"
        }}
    ],
    "existing_strengths": ["Strength 1", "Strength 2"],
    "quick_wins": [
        "Skills you can learn quickly to improve candidacy"
    ],
    "long_term_development": [
        "Skills for career growth in this role"
    ],
    "overall_readiness": "Ready to apply / Need 1-2 skills / Need significant upskilling"
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a career development advisor helping students identify skill gaps and create learning plans."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.6
        )

        response_text = response.choices[0].message.content
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        return json.loads(response_text)

    except Exception as e:
        print(f"Skills gap analysis error: {e}")
        return None
