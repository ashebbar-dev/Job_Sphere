import openai
import os
import json
from datetime import datetime, timedelta, timezone
from models import db, Company

def research_company(company_name, company_website=None):
    """
    Deep research on company using AI
    Returns: dict with company insights
    """
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Check if we have cached research (less than 7 days old)
    company = Company.query.filter_by(name=company_name).first()
    if company and company.research_data and company.last_researched:
        if datetime.now(timezone.utc) - company.last_researched.replace(tzinfo=timezone.utc) < timedelta(days=7):
            return company.research_data

    # Perform research
    prompt = f"""Research the company "{company_name}" {f'(website: {company_website})' if company_website else ''}.

Provide a comprehensive analysis in the following JSON format:
{{
    "company_overview": "Brief description of the company",
    "industry": "Primary industry",
    "company_size": "Estimated employee count or company size",
    "culture_values": ["value1", "value2", "value3"],
    "tech_stack": ["tech1", "tech2", "tech3"],
    "recent_news": ["news1", "news2"],
    "work_environment": "Description of work culture",
    "key_facts": ["fact1", "fact2", "fact3"]
}}

Focus on information relevant for job seekers. If you cannot find specific information, use "Unknown" or empty arrays."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a company research analyst helping job seekers understand potential employers."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )

        # Parse JSON response
        response_text = response.choices[0].message.content
        # Extract JSON from potential markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        research_data = json.loads(response_text)

        # Cache the research
        if company:
            company.research_data = research_data
            company.last_researched = datetime.now(timezone.utc)
            db.session.commit()

        return research_data

    except Exception as e:
        print(f"Company research error: {e}")
        return {
            "company_overview": f"Research data unavailable for {company_name}",
            "industry": "Unknown",
            "company_size": "Unknown",
            "culture_values": [],
            "tech_stack": [],
            "recent_news": [],
            "work_environment": "Unknown",
            "key_facts": []
        }

def analyze_job_requirements(job_description, job_requirements):
    """
    Extract and analyze key requirements from job posting
    """
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f"""Analyze this job posting and extract key requirements:

Job Description:
{job_description}

Additional Requirements:
{json.dumps(job_requirements, indent=2)}

Provide analysis in JSON format:
{{
    "required_skills": ["skill1", "skill2"],
    "preferred_skills": ["skill3", "skill4"],
    "experience_level": "entry/mid/senior",
    "key_responsibilities": ["resp1", "resp2"],
    "must_have_keywords": ["keyword1", "keyword2"],
    "nice_to_have_keywords": ["keyword3", "keyword4"]
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a job posting analyst specializing in extracting key requirements for candidates."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.5
        )

        response_text = response.choices[0].message.content
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        return json.loads(response_text)

    except Exception as e:
        print(f"Job analysis error: {e}")
        return None
