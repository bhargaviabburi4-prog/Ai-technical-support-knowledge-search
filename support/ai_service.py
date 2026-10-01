import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def generate_ai_answer(user_question, articles):
    """
    Generates a beginner-friendly solution using Gemini API based on 
    retrieved knowledge base articles. If API key is missing or API fails,
    provides a structured fallback answer directly from the database.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '').strip()
    
    # Check if articles were retrieved
    if articles and len(articles) > 0:
        articles_text = "\n\n".join([
            f"--- ARTICLE #{idx+1} ---\n"
            f"Title: {art.title}\n"
            f"Category: {art.category}\n"
            f"Problem Description: {art.problem}\n"
            f"Knowledge Solution: {art.solution}\n"
            f"Keywords: {art.keywords}"
            for idx, art in enumerate(articles)
        ])
        db_coverage_note = ""
    else:
        articles_text = "No matching knowledge base articles were found in our internal database."
        db_coverage_note = "NOTE: The internal database does not contain a specific article for this issue."

    # If no API key is provided, use DB fallback
    if not api_key or api_key == "your_gemini_api_key_here":
        return generate_db_fallback_response(user_question, articles, note="Gemini API key is not configured in .env. Showing direct database knowledge.")

    system_prompt = (
        "You are an empathetic, clear, and beginner-friendly AI Technical Support Specialist.\n"
        "Your job is to answer user technical support questions based strictly on the provided Knowledge Base articles.\n\n"
        "CRITICAL INSTRUCTIONS:\n"
        "1. Use the retrieved knowledge base articles as your PRIMARY source of truth.\n"
        "2. Do NOT invent technical steps, commands, or details that contradict the knowledge base.\n"
        "3. Explain the solution in simple, easy-to-understand language suitable for a non-technical user.\n"
        "4. Structure your response into clear Markdown sections with these exact headings:\n"
        "   - ### Short Explanation\n"
        "   - ### Possible Cause\n"
        "   - ### Step-by-Step Solution\n"
        "   - ### Recommended Action\n"
        "5. If the database knowledge articles do not contain enough information for the exact question, clearly include this disclaimer at the beginning of your response:\n"
        "   '⚠️ *Note: Our knowledge base has limited specific details for this query. Below is a general troubleshooting guide based on available technical standards.*'\n\n"
        f"RETRIEVED KNOWLEDGE BASE ARTICLES:\n{articles_text}\n\n"
        f"USER QUESTION: {user_question}"
    )

    # Try SDK 1: google.genai
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=system_prompt,
        )
        if response and hasattr(response, 'text') and response.text:
            return {
                'explanation': response.text,
                'source': 'Gemini AI (Powered by Database Knowledge)',
                'is_ai': True
            }
    except Exception as e1:
        logger.warning(f"google.genai SDK failed: {e1}, trying google.generativeai...")
        # Try SDK 2: google.generativeai
        try:
            # pyrefly: ignore [missing-import]
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=api_key)
            model = genai_legacy.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(system_prompt)
            if response and hasattr(response, 'text') and response.text:
                return {
                    'explanation': response.text,
                    'source': 'Gemini AI (Powered by Database Knowledge)',
                    'is_ai': True
                }
        except Exception as e2:
            logger.error(f"Both Gemini SDK attempts failed: {e2}")

    # Fallback if AI fails or errors out
    return generate_db_fallback_response(user_question, articles, note="AI service is currently offline/unavailable. Displaying direct Database Knowledge Solution.")


def generate_db_fallback_response(user_question, articles, note=""):
    """
    Generates a structured fallback response directly from database articles.
    """
    if not articles or len(articles) == 0:
        explanation = (
            f"{note}\n\n"
            "### Short Explanation\n"
            "No direct match was found in the Technical Support Knowledge Base for your question.\n\n"
            "### Possible Cause\n"
            "The specific issue or keywords entered may not yet be indexed in our database system.\n\n"
            "### Step-by-Step Solution\n"
            "1. Try rephrasing your search using common technical keywords (e.g. 'Wi-Fi', 'Python', 'Printer', 'Git', 'Windows').\n"
            "2. Browse all available articles in the Knowledge Base directory.\n"
            "3. Contact a system administrator via the Django Admin panel to add an article for this topic.\n\n"
            "### Recommended Action\n"
            "Check network cables, restart your software/device, or query the Knowledge Directory."
        )
    else:
        main_art = articles[0]
        explanation = (
            f"*{note}*\n\n"
            f"### Short Explanation\n"
            f"Based on article **'{main_art.title}'**, here is the solution for your issue.\n\n"
            f"### Possible Cause\n"
            f"{main_art.problem}\n\n"
            f"### Step-by-Step Solution\n"
            f"{main_art.solution}\n\n"
            f"### Recommended Action\n"
            f"Follow the steps above carefully. If issue persists, check related articles below or consult system support."
        )

    return {
        'explanation': explanation,
        'source': 'Django Database (Offline / Fallback Mode)',
        'is_ai': False
    }
