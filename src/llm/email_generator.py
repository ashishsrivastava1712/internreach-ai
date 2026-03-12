import os
import json
import time
import re
from openai import OpenAI
from src.rag.vector_store import retrieve_relevant_chunks

# ── Config ────────────────────────────────────
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = "https://api.groq.com/openai/v1"
CANDIDATE_NAME  = "Ashish Srivastava"
CANDIDATE_EMAIL = "ashish171200@gmail.com"
MODEL           = "llama-3.3-70b-versatile"

try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
    OPENAI_API_KEY  = os.environ.get("OPENAI_API_KEY",  OPENAI_API_KEY)
    OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", OPENAI_BASE_URL)
    CANDIDATE_NAME  = os.environ.get("CANDIDATE_NAME",  CANDIDATE_NAME)
    CANDIDATE_EMAIL = os.environ.get("CANDIDATE_EMAIL", CANDIDATE_EMAIL)
    MODEL           = os.environ.get("LLM_MODEL",       MODEL)
except:
    pass

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)


def _clean_json(text: str) -> dict:
    text = re.sub(r'```json|```', '', text).strip()
    start = text.find("{")
    end   = text.rfind("}") + 1
    if start != -1 and end > start:
        text = text[start:end]
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return json.loads(text)


def generate_email(hr: dict, extra_instruction: str = "") -> dict:
    query   = f"skills and projects relevant to {hr['domain']} internship at {hr['company']}"
    context = retrieve_relevant_chunks(query, k=3)

    prompt = f"""You are helping {CANDIDATE_NAME} apply for internships.

Write a professional internship application email:
- FROM: {CANDIDATE_NAME} ({CANDIDATE_EMAIL})
- TO: {hr['hr_name']} at {hr['company']} ({hr['domain']} domain)
- Resume highlights: {context[:400]}

Rules:
1. Sign ONLY as "{CANDIDATE_NAME}" — never use placeholders like [Your Name]
2. Mention 1-2 specific skills from resume highlights
3. 150-200 words, professional and warm tone
4. End with a call to action

{extra_instruction}

Return ONLY valid JSON (no markdown, no extra text):
{{"subject": "your subject here", "body": "your email body here"}}"""

    for attempt in range(1, 4):
        try:
            response = client.chat.completions.create(
                model       = MODEL,
                messages    = [{"role": "user", "content": prompt}],
                temperature = 0.7,
                max_tokens  = 800
            )

            if not response or not response.choices:
                time.sleep(5)
                continue

            content = response.choices[0].message.content
            if not content:
                time.sleep(5)
                continue

            result = _clean_json(content)

            if "subject" in result and "body" in result:
                result["body"]    = result["body"].replace("[Your Name]", CANDIDATE_NAME)
                result["subject"] = result["subject"].replace("[Your Name]", CANDIDATE_NAME)
                result["retrieved_context"] = context
                return result

        except json.JSONDecodeError:
            print(f"   ⚠️  JSON error, retrying... ({attempt}/3)")
            time.sleep(5)
        except Exception as e:
            error_str = str(e)
            if "429" in error_str:
                print(f"   ⚠️  Rate limited. Waiting 30s...")
                time.sleep(30)
            else:
                print(f"   ❌ Error: {error_str[:100]}")
                time.sleep(5)

    # Fallback template
    return {
        "subject": f"Internship Application — {hr['domain']} at {hr['company']}",
        "body": f"""Dear {hr['hr_name']},

I hope this message finds you well. My name is {CANDIDATE_NAME}, and I am writing to express my strong interest in an internship opportunity at {hr['company']}.

With hands-on experience in Python, Machine Learning, and Deep Learning, I believe I can contribute meaningfully to your {hr['domain']} team. I have worked on projects involving data analysis and model development that closely align with {hr['company']}'s focus areas.

I would welcome the opportunity to discuss how my background aligns with your goals. Please find my resume attached for your reference.

Thank you for your time and consideration.

Best regards,
{CANDIDATE_NAME}
{CANDIDATE_EMAIL}""",
        "retrieved_context": context
    }