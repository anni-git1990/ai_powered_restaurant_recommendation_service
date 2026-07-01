import os
import json

# Manually load the env file for testing
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip()

from src.schemas import RecommendationRequest
from src.main import get_recommendations

def test():
    req = RecommendationRequest(
        location="Banashankari",
        budget="medium",
        cuisine="North Indian",
        min_rating=4.0,
        extra_preferences="I love spicy food and a cozy ambiance. It would be great if they serve good desserts."
    )
    
    print("Sending test request to recommendation engine...")
    print(f"Request: {req.model_dump_json(indent=2)}")
    
    try:
        response = get_recommendations(req)
        print("\n--- AI Recommendation Response ---")
        print(response.model_dump_json(indent=2))
    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    test()
