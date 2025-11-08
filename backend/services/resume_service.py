import json
import os
import re
from io import BytesIO
from textwrap import wrap

import PyPDF2
import openai
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def _parse_openai_json(response):
    """Normalize OpenAI response objects (client or raw dict) into JSON."""
    response_text = None

    if isinstance(response, dict):
        response_text = response.get("output_text")
        if not response_text:
            fragments = []
            for item in response.get("output", []):
                content_list = item.get("content", [])
                for content in content_list:
                    if content.get("type") == "output_text":
                        fragments.append(content.get("text", ""))
            response_text = "".join(fragments)
        if not response_text and response.get("choices"):
            try:
                response_text = response["choices"][0]["message"]["content"]
            except (KeyError, IndexError, TypeError):
                response_text = None
    else:
        response_text = getattr(response, "output_text", None)
        if not response_text:
            try:
                fragments = []
                for item in getattr(response, "output", []):
                    for content in getattr(item, "content", []):
                        if getattr(content, "type", "") == "output_text":
                            fragments.append(content.text)
                response_text = "".join(fragments)
            except AttributeError:
                response_text = None
        if not response_text and hasattr(response, "choices"):
            try:
                response_text = response.choices[0].message.content
            except (AttributeError, IndexError):
                response_text = None

    if not response_text or not str(response_text).strip():
        raise ValueError("OpenAI response did not include text output")

    cleaned = str(response_text).strip()
    if "```json" in cleaned:
        cleaned = cleaned.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in cleaned:
        cleaned = cleaned.split("```", 1)[1].split("```", 1)[0].strip()

    return json.loads(cleaned)

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

    base_prompt = (
        "You are a meticulous resume parsing assistant. Extract only verifiable facts from the resume. "
        "Return a JSON object matching the required structure with arrays where appropriate. "
        'If a field is missing use the string "Not mentioned" or an empty array.'
    )

    user_prompt = f"""Resume:
{resume_text}

Required JSON structure:
{{
    "name": "Full name",
    "email": "Email address",
    "phone": "Phone number",
    "location": "Location if mentioned",
    "links": ["Relevant portfolio or profile links"],
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
}}"""

    # Use Chat Completions API with GPT-4o (supports JSON mode)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": base_prompt,
                },
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=2000,
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        return _parse_openai_json(response)
    except Exception as error:
        print(f"Resume parsing error: {error}")
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
            model="gpt-4o",
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
            model="gpt-4o",
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

def personalize_resume(
    student_resume,
    job_analysis,
    company_research,
    match_analysis,
    skills_gap=None,
):
    """Generate structured personalized resume content ready for templating."""
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""Create a personalized resume content package for this job application.

Original Resume Data (authoritative facts only):
{json.dumps(student_resume, indent=2)}

Job Requirements:
{json.dumps(job_analysis, indent=2)}

Company & Role Research:
{json.dumps(company_research, indent=2)}

Match Analysis Insights:
{json.dumps(match_analysis, indent=2)}

Skills Gap Analysis:
{json.dumps(skills_gap or {}, indent=2)}

Rules:
- Do not fabricate experience, dates, titles, or companies.
- Only use information supplied above.
- Tailor language to mirror the company's tone and highlight the most relevant achievements.
- Keep bullet points outcome-focused with metrics or impact where present in the source data.

Return strict JSON with this schema:
{{
    "professional_summary": "2-3 sentence summary aligned to the target company",
    "branding_headline": "Short headline that sells the candidate for this specific role",
    "key_highlights": ["3 bullet statements quantifying major wins relevant to the role"],
    "skills_section": {{
        "primary_skills": ["Skills that map directly to must-have requirements"],
        "secondary_skills": ["Supporting or complementary skills"],
        "tooling": ["Specific tools, platforms, or methodologies cited in the resume"]
    }},
    "experience_section": [
        {{
            "title": "Role title from resume",
            "company": "Company from resume",
            "duration": "Duration from resume",
            "impact_bullets": [
                "Tailored bullet written in action-result format grounded in resume facts"
            ],
            "tech_stack": ["Technologies used if available"]
        }}
    ],
    "projects_section": [
        {{
            "name": "Project name",
            "description": "1-2 sentence description highlighting relevance",
            "impact_bullets": [
                "Tailored outcomes or learnings"
            ],
            "tech_stack": ["Technologies if mentioned"]
        }}
    ],
    "education_section": [
        {{
            "degree": "Degree title",
            "institution": "Institution",
            "year": "Graduation year",
            "highlights": ["Notable coursework or achievements relevant to the role"]
        }}
    ],
    "certifications": ["Certification names pulled from resume"],
    "tailoring_notes": {{
        "culture_fit": ["Talking points to demonstrate alignment with company values"],
        "interview_talking_points": ["Topics the candidate should be ready to discuss"],
        "ats_keywords": ["High-priority keywords to preserve in the resume"]
    }}
}}

Respond with valid JSON only."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional resume writer specializing in tailoring resumes for specific job applications.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=2500,
            temperature=0.65,
        )

        response_text = response.choices[0].message.content
        if "```json" in response_text:
            response_text = (
                response_text.split("```json")[1].split("```")[0].strip()
            )
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
            model="gpt-4o",
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


def _safe_token(value, fallback):
    """Sanitize a value for filesystem usage."""
    token = (value or "").strip()
    if not token:
        token = fallback
    sanitized = re.sub(r"[^A-Za-z0-9]+", "-", token)
    sanitized = sanitized.strip("-").lower()
    return sanitized or fallback


def get_personalized_resume_path(student, drive):
    """Compute deterministic path for a student's personalized resume PDF."""
    base_dir = os.path.join("uploads", "resumes", "personalized")
    os.makedirs(base_dir, exist_ok=True)

    enrollment_token = _safe_token(
        getattr(student, "enrollment_no", None), f"student-{student.id}"
    )
    filename = f"{enrollment_token}-drive-{drive.id}.pdf"
    return os.path.join(base_dir, filename)


def _wrap_paragraphs(text, width_chars):
    lines = []
    for paragraph in (text or "").splitlines():
        if not paragraph.strip():
            lines.append("")
            continue
        lines.extend(wrap(paragraph.strip(), width_chars))
    return lines


def _draw_text_block(canvas_obj, text, x, y, width, font_size=10, leading=14):
    """Render wrapped text and return new y position."""
    max_chars = max(50, int(width / (font_size * 0.55)))
    lines = _wrap_paragraphs(text, max_chars)

    text_obj = canvas_obj.beginText(x, y)
    text_obj.setFont("Helvetica", font_size)
    for line in lines:
        if y <= 72:
            canvas_obj.drawText(text_obj)
            canvas_obj.showPage()
            y = letter[1] - 72
            text_obj = canvas_obj.beginText(x, y)
            text_obj.setFont("Helvetica", font_size)
        text_obj.textLine(line)
        y = text_obj.getY()

    canvas_obj.drawText(text_obj)
    return y


def _draw_bullet_list(canvas_obj, items, x, y, width, font_size=10, leading=14):
    max_chars = max(50, int((width - 16) / (font_size * 0.55)))

    for item in items or []:
        content_lines = _wrap_paragraphs(str(item), max_chars)
        if not content_lines:
            continue

        for idx, line in enumerate(content_lines):
            if y <= 72:
                canvas_obj.showPage()
                y = letter[1] - 72
            canvas_obj.setFont("Helvetica", font_size)
            if idx == 0:
                canvas_obj.drawString(x, y, "•")
                canvas_obj.drawString(x + 12, y, line)
            else:
                canvas_obj.drawString(x + 12, y, line)
            y -= leading
        y -= 2

    return y


def generate_personalized_resume_pdf(student, drive, personalized_content, file_path=None):
    """Render personalized resume content into a polished PDF template."""
    if not personalized_content:
        return None

    if not file_path:
        file_path = get_personalized_resume_path(student, drive)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    pdf = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    margin = 50
    x_start = margin
    content_width = width - 2 * margin
    y = height - margin

    # Header
    pdf.setFillColor(colors.HexColor("#0f172a"))
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(
        x_start,
        y,
        personalized_content.get("header", {}).get("name")
        or getattr(student, "name", "Student"),
    )
    pdf.setFillColor(colors.black)
    y -= 24

    contact_segments = []
    header = personalized_content.get("header", {})
    if header.get("email"):
        contact_segments.append(header["email"])
    if header.get("phone"):
        contact_segments.append(header["phone"])
    if header.get("location"):
        contact_segments.append(header["location"])
    if header.get("links"):
        contact_segments.extend(header["links"])

    if contact_segments:
        pdf.setFont("Helvetica", 10)
        pdf.drawString(x_start, y, " • ".join(contact_segments))
        y -= 18

    if personalized_content.get("branding_headline"):
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x_start, y, personalized_content["branding_headline"])
        y -= 18

    # Helper to draw section heading
    def draw_section(title, current_y):
        nonlocal pdf
        if current_y <= margin + 40:
            pdf.showPage()
            current_y = height - margin
        pdf.setFont("Helvetica-Bold", 12)
        pdf.setFillColor(colors.HexColor("#1d4ed8"))
        pdf.drawString(x_start, current_y, title.upper())
        pdf.setFillColor(colors.black)
        return current_y - 18

    y = draw_section("Professional Summary", y)
    y = _draw_text_block(pdf, personalized_content.get("professional_summary", ""), x_start, y, content_width)
    y -= 10

    if personalized_content.get("key_highlights"):
        y = draw_section("Key Highlights", y)
        y = _draw_bullet_list(pdf, personalized_content["key_highlights"], x_start, y, content_width)
        y -= 6

    skills_section = personalized_content.get("skills_section") or {}
    if any(skills_section.get(key) for key in ["primary_skills", "secondary_skills", "tooling"]):
        y = draw_section("Skills Alignment", y)
        segments = []
        if skills_section.get("primary_skills"):
            segments.append(f"Primary: {', '.join(skills_section['primary_skills'])}")
        if skills_section.get("secondary_skills"):
            segments.append(f"Secondary: {', '.join(skills_section['secondary_skills'])}")
        if skills_section.get("tooling"):
            segments.append(f"Tooling: {', '.join(skills_section['tooling'])}")
        y = _draw_bullet_list(pdf, segments, x_start, y, content_width)
        y -= 6

    experience_section = personalized_content.get("experience_section") or []
    if experience_section:
        y = draw_section("Experience", y)
        for exp in experience_section:
            if y <= margin + 80:
                pdf.showPage()
                y = height - margin
            pdf.setFont("Helvetica-Bold", 11)
            exp_title = " — ".join(filter(None, [exp.get("title"), exp.get("company")]))
            pdf.drawString(x_start, y, exp_title or "Experience")
            y -= 14

            if exp.get("duration"):
                pdf.setFont("Helvetica-Oblique", 9)
                pdf.drawString(x_start, y, exp["duration"])
                y -= 14

            if exp.get("impact_bullets"):
                y = _draw_bullet_list(pdf, exp["impact_bullets"], x_start, y, content_width)
            if exp.get("tech_stack"):
                pdf.setFont("Helvetica", 9)
                pdf.drawString(x_start, y, f"Tech: {', '.join(exp['tech_stack'])}")
                y -= 14

            y -= 6

    projects_section = personalized_content.get("projects_section") or []
    if projects_section:
        y = draw_section("Projects", y)
        for project in projects_section:
            if y <= margin + 80:
                pdf.showPage()
                y = height - margin
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(x_start, y, project.get("name", "Project"))
            y -= 14
            pdf.setFont("Helvetica", 10)
            y = _draw_text_block(pdf, project.get("description", ""), x_start, y, content_width)
            if project.get("impact_bullets"):
                y = _draw_bullet_list(pdf, project["impact_bullets"], x_start, y, content_width)
            if project.get("tech_stack"):
                pdf.setFont("Helvetica", 9)
                pdf.drawString(x_start, y, f"Tech: {', '.join(project['tech_stack'])}")
                y -= 14
            y -= 6

    education_section = personalized_content.get("education_section") or []
    if education_section:
        y = draw_section("Education", y)
        for edu in education_section:
            if y <= margin + 60:
                pdf.showPage()
                y = height - margin
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(
                x_start,
                y,
                " — ".join(filter(None, [edu.get("degree"), edu.get("institution")])),
            )
            y -= 14
            if edu.get("year"):
                pdf.setFont("Helvetica-Oblique", 9)
                pdf.drawString(x_start, y, str(edu["year"]))
                y -= 14
            if edu.get("highlights"):
                y = _draw_bullet_list(pdf, edu["highlights"], x_start, y, content_width)
            y -= 4

    if personalized_content.get("certifications"):
        y = draw_section("Certifications", y)
        y = _draw_bullet_list(pdf, personalized_content["certifications"], x_start, y, content_width)
        y -= 4

    tailoring_notes = personalized_content.get("tailoring_notes") or {}
    note_items = []
    if tailoring_notes.get("culture_fit"):
        note_items.append("Culture Fit: " + "; ".join(tailoring_notes["culture_fit"]))
    if tailoring_notes.get("interview_talking_points"):
        note_items.append(
            "Interview Talking Points: "
            + "; ".join(tailoring_notes["interview_talking_points"])
        )
    if tailoring_notes.get("ats_keywords"):
        note_items.append("ATS Keywords: " + ", ".join(tailoring_notes["ats_keywords"]))

    if note_items:
        y = draw_section("Tailoring Notes", y)
        y = _draw_bullet_list(pdf, note_items, x_start, y, content_width)

    pdf.save()
    return file_path


def prepare_personalized_resume(
    student,
    drive,
    parsed_resume,
    job_analysis,
    company_research,
    match_analysis,
    skills_gap,
):
    """Generate personalized resume content and rendered PDF."""
    if not student or not drive:
        return None, None

    header = {
        "name": parsed_resume.get("name") or getattr(student, "name", ""),
        "email": parsed_resume.get("email") or getattr(student.user, "email", ""),
        "phone": parsed_resume.get("phone") or getattr(student, "phone", ""),
        "links": parsed_resume.get("links", []),
        "location": parsed_resume.get("location"),
    }

    personalized_content = personalize_resume(
        {**parsed_resume, "header": header},
        job_analysis,
        company_research,
        match_analysis,
        skills_gap=skills_gap,
    )

    if personalized_content is None:
        return None, None

    # Ensure header metadata is preserved for PDF generation.
    personalized_content.setdefault("header", header)

    pdf_path = generate_personalized_resume_pdf(student, drive, personalized_content)

    return personalized_content, pdf_path
