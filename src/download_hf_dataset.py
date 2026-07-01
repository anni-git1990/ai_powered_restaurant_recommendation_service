import os
import pandas as pd
from datasets import load_dataset

def main():
    print("Loading dataset from Hugging Face...")
    # Load the dataset from Hugging Face
    dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train", token=os.environ.get("HF_TOKEN"))
    
    # Convert to pandas DataFrame for easier review and preprocessing
    df = dataset.to_pandas()
    
    print("\n--- Initial Review ---")
    print("Initial Data Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("Missing values per column:\n", df.isnull().sum())
    
    print("\n--- Preprocessing ---")
    # Drop completely duplicated rows
    initial_len = len(df)
    df = df.drop_duplicates()
    print(f"Dropped {initial_len - len(df)} duplicate rows.")
    
    # Fill or drop nulls if strictly required (we'll just drop rows where 'name' is missing, for example)
    if 'name' in df.columns:
        df = df.dropna(subset=['name'])
    
    print("Preprocessed Data Shape:", df.shape)
    
    # Save to parquet
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "zomato_hf.parquet")
    
    print(f"\nSaving to {output_path}...")
    df.to_parquet(output_path, index=False)
    print("Data successfully saved in parquet format!")

if __name__ == "__main__":
    main()
