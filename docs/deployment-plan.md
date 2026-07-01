# Deployment Plan: Zomato AI Restaurant Recommendation Service

This document details the step-by-step instructions to deploy the FastAPI backend to **Railway** and the React (Vite) frontend to **Vercel**.

---

## Production Architecture

Below is the high-level production architecture for the Zomato AI Restaurant Recommendation system:

```mermaid
graph TD
    User[Client Browser]
    
    subgraph Vercel ["Vercel Hosting"]
        FE["React Frontend App (Vite)"]
    end
    
    subgraph Railway ["Railway Cloud"]
        BE["FastAPI Backend App"]
        LocalCache[("Local Disk (data/zomato_hf.parquet)")]
    end
    
    subgraph External ["External Services"]
        HF["Hugging Face Hub"]
        Groq["Groq Cloud API (LLM)"]
    end
    
    User -->|Accesses UI via HTTPS| FE
    User -->|API requests (CORS)| BE
    BE -->|Checks/Downloads Dataset| HF
    HF -.->|Saves dataset| LocalCache
    BE -->|Reads & Filters candidates| LocalCache
    BE -->|Submits candidates & prompt| Groq
    Groq -->|Returns ranked JSON recommendations| BE
```

### Architectural Key Points:
1. **Frontend Hosting (Vercel)**: Serves static assets, routes pages, and executes frontend business logic inside the user's browser. It uses the `VITE_API_BASE_URL` environment variable to identify and talk to the backend.
2. **Backend API (Railway)**: A containerized Python instance running FastAPI. Exposed via a public URL on port `8000`. Handles requests from Vercel using configured CORS middleware.
3. **Data Storage & Self-Healing Cache**: A SQLite database/parquet file cache. Upon container startup, the FastAPI app checks if `data/zomato_hf.parquet` is present on the disk. If missing, it fetches the raw dataset dynamically from Hugging Face and caches it locally.
4. **AI Reasoning (Groq)**: The backend filters local restaurants down to a small pool (<20) and sends a context-rich prompt to the Groq API. Groq ranks them and returns the final structured recommendations to the backend.

---

## 1. Backend Deployment (Railway)

We deploy the FastAPI backend on Railway. Thanks to the automatic download integration, the server will fetch the Hugging Face dataset on startup without requiring any manual database setup.

### Prerequisites & Configurations
* **Source Directory:** Root directory of the repository.
* **Build tool:** Nixpacks / Buildpack (Auto-detected).
* **Process Configuration:** Handled by [Procfile](file:///d:/anita/product-AI-training/git_projects/ai_powered_restaurant_recommendation_service/Procfile):
  ```text
  web: uvicorn src.main:app --host 0.0.0.0 --port $PORT
  ```

### Step-by-Step Instructions
1. Log in to [Railway.app](https://railway.app/).
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select your repository `ai_powered_restaurant_recommendation_service`.
4. Railway will analyze the repository and detect the python app.
5. Before deploying finishes, click on the service settings and navigate to the **Variables** tab.
6. Add the following environment variables:
   * `GROQ_API_KEY`: `your_actual_groq_api_key`
   * `PORT`: `8000` (Optional; Railway automatically injects this value, but setting it explicitly is safe).
7. Under the **Settings** tab, make sure the **Start Command** is empty or set to use the Procfile.
8. Click **Deploy**.
9. Once the build completes, Railway will assign a public domain (e.g. `https://xxx.up.railway.app`). Go to **Settings** -> **Public Networking** to find or generate the domain. Note down this URL as you will need it for the frontend deployment.

> [!NOTE]
> During the first deploy, the startup log will show `Dataset not found at data/zomato_hf.parquet. Initiating download...`. It will automatically fetch the ~147MB dataset from Hugging Face. This may take 30–60 seconds. Subsequent server restarts won't download it again if the server container is persisted, but Railway containers are ephemeral so the startup auto-download ensures the API is always self-healing.

---

## 2. Frontend Deployment (Vercel)

We deploy the React frontend on Vercel.

### Prerequisites & Configurations
* **Framework Preset:** Vite
* **Root Directory:** `frontend`
* **Build Command:** `npm run build`
* **Output Directory:** `dist`

### Step-by-Step Instructions
1. Log in to [Vercel.com](https://vercel.com/).
2. Click **Add New** -> **Project**.
3. Import your repository `ai_powered_restaurant_recommendation_service`.
4. In the configuration step:
   * **Root Directory:** Click **Edit** and select the `frontend` folder.
   * **Framework Preset:** Vite (Vercel should auto-detect this).
5. Expand the **Environment Variables** section and add:
   * `VITE_API_BASE_URL`: The public URL of your Railway backend (e.g., `https://xxx.up.railway.app` without a trailing slash).
6. Click **Deploy**.
7. Vercel will build the project and output a production URL (e.g., `https://xxx.vercel.app`).

---

## 3. Verification

Once both services are deployed, perform the following verification checks:

### Backend Health Check
* Open `https://<your-railway-url>/health` in your browser.
* You should receive:
  ```json
  {"status": "healthy"}
  ```
* Open `https://<your-railway-url>/docs` to view the interactive Swagger documentation.

### Frontend Integration Check
* Open the deployed Vercel URL.
* Try searching for a cuisine (e.g., Chinese) and location.
* Verify that the dropdown list loads locations from the backend `/api/locations` endpoint.
* Submit a search and verify that AI recommendations and candidate restaurants load correctly.
