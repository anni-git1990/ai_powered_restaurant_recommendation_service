import os
import pandas as pd
import urllib.request
from io import BytesIO

def main():
    print("Loading dataset from Hugging Face...")
    urls = [
        "https://huggingface.co/api/datasets/ManikaSaini/zomato-restaurant-recommendation/parquet/default/train/0.parquet",
        "https://huggingface.co/api/datasets/ManikaSaini/zomato-restaurant-recommendation/parquet/default/train/1.parquet"
    ]
    
    dfs = []
    token = os.environ.get("HF_TOKEN")
    
    for i, url in enumerate(urls):
        print(f"Downloading chunk {i+1} of {len(urls)} from HF...")
        req = urllib.request.Request(url)
        if token:
            req.add_header("Authorization", f"Bearer {token}")
            
        try:
            with urllib.request.urlopen(req) as response:
                content = response.read()
                df_chunk = pd.read_parquet(BytesIO(content))
                print(f"Chunk {i+1} loaded successfully. Shape: {df_chunk.shape}")
                dfs.append(df_chunk)
        except Exception as e:
            print(f"Error downloading chunk {i+1}: {e}")
            raise e
            
    if not dfs:
        raise ValueError("No data could be downloaded.")
        
    df = pd.concat(dfs, ignore_index=True)
    
    print("\n--- Initial Review ---")
    print("Initial Data Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    
    print("\n--- Preprocessing ---")
    # Drop completely duplicated rows
    initial_len = len(df)
    df = df.drop_duplicates()
    print(f"Dropped {initial_len - len(df)} duplicate rows.")
    
    # Fill or drop nulls if strictly required
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
