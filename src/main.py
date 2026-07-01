import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Manually load the env file for the API
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip()

# Auto-download dataset if not present
if not os.path.exists('data/zomato_hf.parquet'):
    print("Dataset not found at data/zomato_hf.parquet. Initiating download...")
    try:
        from src.download_hf_dataset import main as download_main
        download_main()
    except Exception as e:
        print(f"Error downloading dataset on startup: {e}")


from src.schemas import RecommendationRequest, RecommendationResponse
from src.services import get_filtered_restaurants, get_all_locations
from src.llm import get_ai_recommendations

app = FastAPI(
    title="Zomato AI Recommendation System",
    description="API for the AI-Powered Restaurant Recommendation Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy"}

@app.get("/api/locations")
def get_locations():
    """Returns a list of all available locations."""
    try:
        return {"locations": get_all_locations()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recommend", response_model=RecommendationResponse)
def get_recommendations(req: RecommendationRequest):
    """
    Accepts user dining preferences and returns a filtered list of candidate restaurants.
    This fulfills Phase 2 (Filtering Engine) before LLM Integration.
    """
    try:
        candidates = get_filtered_restaurants(
            location=req.location,
            min_rating=req.min_rating,
            cuisine=req.cuisine,
            budget=req.budget,
            limit=20
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        
    if not candidates:
        raise HTTPException(status_code=404, detail="No restaurants found matching your exact criteria. Please try loosening your constraints.")
        
    # Phase 3: AI Ranking and Explanation
    ranked_candidates = get_ai_recommendations(req, candidates)
        
    return RecommendationResponse(candidates=ranked_candidates)
