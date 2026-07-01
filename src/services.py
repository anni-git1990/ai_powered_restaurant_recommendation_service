import pandas as pd
import re
import os
import ast

DATA_PATH = 'data/zomato_hf.parquet'

def parse_rating(rate_str):
    if not isinstance(rate_str, str): 
        return 0.0
    match = re.search(r'([\d\.]+)/5', rate_str)
    if match: 
        return float(match.group(1))
    return 0.0

def parse_cost(cost_str):
    if not isinstance(cost_str, str): 
        return 0
    # Handle cases like "1,200"
    cleaned = cost_str.replace(',', '').strip()
    if cleaned.isdigit():
        return int(cleaned)
    return 0

def get_filtered_restaurants(location: str, min_rating: float = None, cuisine: str = None, budget: str = None, limit: int = 20):
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Run Phase 1 ingestion first.")
        
    df = pd.read_parquet(DATA_PATH)
    
    if location:
        df = df[df['location'].str.contains(location, case=False, na=False)]
        
    if 'approx_cost(for two people)' in df.columns:
        df = df.rename(columns={'approx_cost(for two people)': 'cost'})
    
    if df.empty:
        return []
        
    # Clean and parse data in Python
    df['parsed_rating'] = df['rate'].apply(parse_rating)
    df['parsed_cost'] = df['cost'].apply(parse_cost)
    
    # 1. Filter by minimum rating
    if min_rating is not None:
        df = df[df['parsed_rating'] >= min_rating]
        
    # 2. Filter by cuisine (case insensitive partial match)
    if cuisine:
        df = df[df['cuisines'].str.contains(cuisine, case=False, na=False)]
        
    # 3. Filter by budget mapping (approx_cost is for two people)
    if budget:
        b = budget.lower().strip()
        if b == 'low':
            df = df[df['parsed_cost'] <= 500]
        elif b == 'medium':
            df = df[(df['parsed_cost'] > 500) & (df['parsed_cost'] <= 1500)]
        elif b == 'high':
            df = df[df['parsed_cost'] > 1500]
            
    # Sort by rating (descending) and then cost (ascending) to get the best value first
    df = df.sort_values(by=['parsed_rating', 'parsed_cost'], ascending=[False, True])
    
    # Remove duplicates by restaurant name (keep the best rated / lowest cost branch/entry)
    df = df.drop_duplicates(subset=['name'], keep='first')
    
    # Extract the Top N limit
    top_df = df.head(limit)
    
    candidates = []
    for _, row in top_df.iterrows():
        cuisines_str = str(row['cuisines'])
        
        # Clean and extract review texts to keep prompt sizes reasonable
        reviews_raw = row.get('reviews_list', '[]')
        reviews = []
        if isinstance(reviews_raw, str) and reviews_raw.strip():
            try:
                reviews_list = ast.literal_eval(reviews_raw)
                for r in reviews_list[:3]:
                    if isinstance(r, tuple) and len(r) > 1:
                        reviews.append(r[1].replace('RATED\n', '').strip()[:200])
            except Exception:
                matches = re.findall(r"RATED\n\s*(.*?)(?=',\s*'Rated|\",\s*\"Rated|'\]|\])", reviews_raw, re.DOTALL)
                reviews = [m.strip()[:200] for m in matches[:3]]
        
        candidates.append({
            "name": row['name'],
            "location": row['location'],
            "cuisines": cuisines_str,
            "rating": row['parsed_rating'],
            "cost": row['parsed_cost'],
            "zomato_url": str(row['url']) if 'url' in row else None,
            "rest_type": str(row['rest_type']) if 'rest_type' in row and pd.notna(row['rest_type']) else None,
            "dish_liked": str(row['dish_liked']) if 'dish_liked' in row and pd.notna(row['dish_liked']) else None,
            "reviews": reviews
        })
        
    return candidates


def get_all_locations():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Run Phase 1 ingestion first.")
        
    df = pd.read_parquet(DATA_PATH)
    locations = df['location'].dropna().unique().tolist()
    return sorted([loc for loc in locations if isinstance(loc, str) and loc.strip()])
