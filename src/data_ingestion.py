import pandas as pd
from datasets import load_dataset
import os

def ingest_data():
    print("Loading Zomato dataset from Hugging Face...")
    try:
        # Load the dataset
        dataset = load_dataset('ManikaSaini/zomato-restaurant-recommendation', token=os.environ.get("HF_TOKEN"))
        # The dataset is usually split, 'train' is the default
        df = dataset['train'].to_pandas()
        
        print(f"Successfully loaded {len(df)} rows. Preprocessing data...")
        
        # 1. Standardize Cuisine text
        if 'Cuisine' in df.columns:
            df['Cuisine'] = df['Cuisine'].astype(str).str.lower().str.strip()
            
        # 2. Normalize cost/prices and ratings if needed
        # Assuming there are standard columns like 'Dining Rating' and 'Prices'
        # We will handle missing values by filling them with 0 or a placeholder
        for col in ['Dining Rating', 'Delivery Rating']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
                
        # Create a data directory in the project root
        os.makedirs('data', exist_ok=True)
        parquet_path = 'data/zomato_hf.parquet'
        
        print(f"Saving cleaned data to Parquet format at {parquet_path}...")
        df.to_parquet(parquet_path, index=False)
        
        
        print("Data ingestion complete!")
        
    except Exception as e:
        print(f"An error occurred during data ingestion: {e}")

if __name__ == "__main__":
    ingest_data()
