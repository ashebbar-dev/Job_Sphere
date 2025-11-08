import json
import os
from datetime import datetime, timedelta, timezone

import openai

from models import Company, db

GENERAL_COMPANY_KEYS = [
    "company_overview",
    "industry",
    "company_size",
    "culture_values",
    "tech_stack",
    "recent_news",
    "work_environment",
    "key_facts",
]


def _parse_response_json(response):
    """Extract JSON string from OpenAI response objects."""
    response_text = getattr(response, "output_text", None)

    if not response_text:
        try:
            parts = []
            for item in getattr(response, "output", []):
                for content in getattr(item, "content", []):
                    if getattr(content, "type", "") == "output_text":
                        parts.append(content.text)
            response_text = "".join(parts)
        except AttributeError:
            response_text = None

    if not response_text and hasattr(response, "choices"):
        # fallback for legacy completion style
        response_text = response.choices[0].message.content

    if not response_text:
        raise ValueError("No text returned from OpenAI response")

    if "```json" in response_text:
        response_text = response_text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in response_text:
        response_text = response_text.split("```", 1)[1].split("```", 1)[0].strip()

    return json.loads(response_text)


def _fallback_company_research(client, company_name, company_website):
    """Use standard GPT-4 completion when deep research is unavailable."""
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
    "key_facts": ["fact1", "fact2", "fact3"],
    "role_insights": {{
        "role_summary": "Unknown",
        "key_responsibilities": [],
        "success_profile": [],
        "emerging_trends": []
    }},
    "tailoring_recommendations": {{
        "resume_focus": [],
        "culture_alignment": [],
        "project_highlights": []
    }}
}}

Focus on information relevant for job seekers. Use "Unknown" or empty arrays if information is not available."""

    fallback = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a company research analyst helping job seekers understand potential employers.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=2000,
        temperature=0.7,
    )

    return _parse_response_json(fallback)


def research_company(
    company_name,
    company_website=None,
    job_title=None,
    job_description=None,
    student_profile=None,
):
    """
    Deep research on company and targeted role using OpenAI Deep Research.
    Returns: dict with company insights and role-tailored recommendations.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    cached_general = None
    company = Company.query.filter_by(name=company_name).first()
    if (
        company
        and company.research_data
        and company.last_researched
        and datetime.now(timezone.utc)
        - company.last_researched.replace(tzinfo=timezone.utc)
        < timedelta(days=7)
    ):
        cached_general = company.research_data

    prompt = f"""You are an elite career intelligence analyst conducting exhaustive research for a student preparing to apply.

Company: {company_name}
Website: {company_website or 'Unknown'}
Target Role: {job_title or 'Not specified'}

Job Description:
{job_description or 'Not provided'}

Student Profile Snapshot (for tailoring suggestions):
{json.dumps(student_profile or {}, indent=2)}

Deliver a comprehensive, factual report using any reputable sources you can find. Structure the final answer strictly as JSON:
{{
    "company_overview": "Two to three sentence overview with mission, product focus, and market position.",
    "industry": "Primary industry or sector",
    "company_size": "Estimated employee count or size band",
    "culture_values": ["Core cultural values in short phrases"],
    "tech_stack": ["Notable technologies or platforms used"],
    "recent_news": ["Important headlines or initiatives from the last 6-12 months"],
    "work_environment": "Description of work culture and collaboration style",
    "key_facts": ["3-5 bullet facts that impress recruiters (awards, growth, customers, etc.)"],
    "role_insights": {{
        "role_summary": "One paragraph explaining what this role is expected to accomplish.",
        "key_responsibilities": ["Concrete responsibilities the role will own"],
        "success_profile": ["Traits or behaviours top performers share"],
        "emerging_trends": ["Market / industry shifts impacting this role right now"]
    }},
    "tailoring_recommendations": {{
        "resume_focus": ["Specific angles this student should emphasize in their resume"],
        "culture_alignment": ["Talking points to show cultural fit"],
        "project_highlights": ["Existing experience or portfolio pieces to spotlight"]
    }},
    "source_notes": ["Short list of sources consulted, if available"]
}}

Return valid JSON only. If credible data cannot be found for any field, use "Unknown" or an empty list."""

    research_data = None

    try:
        # Use OpenAI SDK's responses.create() for deep research with web search
        response = client.responses.create(
            model="o4-mini-deep-research",
            input=prompt,  # Simple string input per Deep Research API docs
            tools=[{"type": "web_search_preview"}],
            reasoning={"summary": "auto"},
            temperature=0.4,
            timeout=600,
        )
        research_data = _parse_response_json(response)
    except Exception as deep_error:
        print(f"Deep research error: {deep_error}")

    if not research_data:
        try:
            research_data = _fallback_company_research(
                client, company_name, company_website
            )
        except Exception as fallback_error:
            print(f"Company research fallback error: {fallback_error}")
            research_data = {
                "company_overview": f"Research data unavailable for {company_name}",
                "industry": "Unknown",
                "company_size": "Unknown",
                "culture_values": [],
                "tech_stack": [],
                "recent_news": [],
                "work_environment": "Unknown",
                "key_facts": [],
                "role_insights": {
                    "role_summary": "Unknown",
                    "key_responsibilities": [],
                    "success_profile": [],
                    "emerging_trends": [],
                },
                "tailoring_recommendations": {
                    "resume_focus": [],
                    "culture_alignment": [],
                    "project_highlights": [],
                },
                "source_notes": [],
            }

    if cached_general:
        # Preserve cached general fields when available to ensure consistency.
        for key in GENERAL_COMPANY_KEYS:
            if key in cached_general and cached_general[key]:
                research_data[key] = cached_general[key]

    # Cache general company data for reuse (exclude job-specific tailoring)
    if company:
        general_payload = {key: research_data.get(key) for key in GENERAL_COMPANY_KEYS}
        company.research_data = general_payload
        company.last_researched = datetime.now(timezone.utc)
        db.session.commit()

    return research_data


def analyze_job_requirements(job_description, job_requirements):
    """
    Extract and analyze key requirements from job posting
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    # Use Chat Completions API with GPT-4o (supports JSON mode)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a job posting analyst specializing in extracting key requirements for candidates. "
                    "Return strict JSON matching the requested schema.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1500,
            temperature=0.3,
            response_format={"type": "json_object"},
        )
        return _parse_response_json(response)
    except Exception as error:
        print(f"Job analysis error: {error}")
        return None
