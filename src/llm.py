import os
import json
import urllib.parse
from groq import Groq
from typing import List, Dict, Any
from src.schemas import RecommendationRequest

# Initialize Groq client. It expects GROQ_API_KEY environment variable to be set.
def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("WARNING: GROQ_API_KEY environment variable not set.")
    return Groq(api_key=api_key)

def get_ai_recommendations(user_req: RecommendationRequest, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not candidates:
        return []
        
    client = get_groq_client()
        
    system_prompt = """You are an expert AI restaurant recommender. 
You will be provided with a user's preferences and a JSON list of restaurant candidates that match their hard constraints, including their cuisines, category/restaurant type, popular dishes, and customer reviews.
Your task is to rank these candidates based on how well they match the user's extra preferences (vibe/requirements), and provide a short, 1-2 sentence personalized explanation for why you recommend each one, citing details from their reviews, dishes, or restaurant type where possible.
If the user has no extra preferences, simply rank them by rating and value, providing a generic but appealing explanation.

CRITICAL INSTRUCTION: You MUST return your response as a JSON object with a single key "recommendations" containing a list of objects. Each object must have "name" (matching the candidate name exactly) and "explanation" (your 1-2 sentence reason). Rank the objects starting with the best match first. Do not truncate or skip any candidates; return an explanation for all provided candidates."""
    
    user_content = f"""
User Preferences:
- Location: {user_req.location}
- Budget: {user_req.budget}
- Cuisine: {user_req.cuisine}
- Min Rating: {user_req.min_rating}
- Extra Preferences: {user_req.extra_preferences}

Candidate Restaurants:
{json.dumps(candidates, indent=2)}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        
        result = json.loads(response.choices[0].message.content)
        ai_recs = result.get("recommendations", [])
        
        rec_map = {rec.get('name').lower().strip(): rec.get('explanation', '') for rec in ai_recs if rec.get('name')}
        
        ranked_candidates = []
        
        # Reorder based on LLM output order
        for ai_rec in ai_recs:
            name = ai_rec.get("name")
            if not name:
                continue
            name_clean = name.lower().strip()
            cand = next((c for c in candidates if c["name"].lower().strip() == name_clean), None)
            if cand:
                # Add the explanation
                new_cand = cand.copy()
                new_cand["explanation"] = ai_rec.get("explanation", "")
                
                # Strip out internal rich fields so we don't pollute the final API response
                new_cand.pop("rest_type", None)
                new_cand.pop("dish_liked", None)
                new_cand.pop("reviews", None)
                
                ranked_candidates.append(new_cand)
                
        # Append any that the LLM missed at the bottom
        for cand in candidates:
            cand_name_clean = cand["name"].lower().strip()
            if not any(rc["name"].lower().strip() == cand_name_clean for rc in ranked_candidates):
                new_cand = cand.copy()
                # See if the LLM provided an explanation under a slightly different name case
                explanation = "Matches your base criteria."
                for ai_rec in ai_recs:
                    if ai_rec.get("name") and ai_rec.get("name").lower().strip() == cand_name_clean:
                        explanation = ai_rec.get("explanation", "Matches your base criteria.")
                        break
                new_cand["explanation"] = explanation
                
                # Strip out internal rich fields
                new_cand.pop("rest_type", None)
                new_cand.pop("dish_liked", None)
                new_cand.pop("reviews", None)
                
                ranked_candidates.append(new_cand)
                
        return ranked_candidates

    except Exception as e:
        print(f"Error parsing LLM response or calling Groq API: {e}")
        # Fallback to returning original candidates with generic explanation
        fallback = []
        for c in candidates:
            new_cand = c.copy()
            new_cand["explanation"] = "Matches your base criteria."
            new_cand.pop("rest_type", None)
            new_cand.pop("dish_liked", None)
            new_cand.pop("reviews", None)
            fallback.append(new_cand)
        return fallback

