from pydantic import BaseModel
from typing import Optional, List

class RecommendationRequest(BaseModel):
    location: str
    budget: Optional[str] = None  # e.g., "low", "medium", "high"
    cuisine: Optional[str] = None
    min_rating: Optional[float] = None
    extra_preferences: Optional[str] = None

class RestaurantCandidate(BaseModel):
    name: str
    location: str
    cuisines: str
    rating: float
    cost: int
    zomato_url: Optional[str] = None
    explanation: Optional[str] = None

class RecommendationResponse(BaseModel):
    candidates: List[RestaurantCandidate]
