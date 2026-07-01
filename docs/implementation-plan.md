# Phase-Wise Implementation Plan: AI-Powered Restaurant Recommendation System

This document outlines the step-by-step execution plan to build the Zomato-inspired recommendation system, as designed in `architecture.md` and `context.md`.

## cfx
**Goal:** Establish the foundation and prepare the restaurant data.

1. **Environment Setup**
   - Initialize the project repository.
   - Set up a Python virtual environment.
   - Install core dependencies: `fastapi`, `uvicorn`, `pandas`, `datasets` (Hugging Face), `groq`, `pydantic`.
2. **Dataset Acquisition**
   - Write a script to download the `ManikaSaini/zomato-restaurant-recommendation` dataset from Hugging Face.
3. **Data Preprocessing & Storage**
   - Clean the raw data: handle missing values, normalize cost/ratings, and standardize text (e.g., lowercase cuisines).
   - Load the cleaned data into the chosen datastore (e.g., an in-memory Pandas DataFrame, SQLite, or a fast key-value store for local MVP).

## Phase 2: Backend API & Filtering Engine
**Goal:** Create the core API and the preliminary filtering logic.

1. **API Skeleton**
   - Set up the FastAPI application.
   - Define Pydantic models for User Request (Location, Budget, Cuisine, Min Rating, Extra Preferences) and the Expected Response.
2. **Filtering Engine (Hard Constraints)**
   - Implement logic to query the datastore based on user inputs.
   - Example: Filter dataset where `Location == user.location` AND `Rating >= user.min_rating` AND `Cuisine includes user.cuisine`.
   - Limit the returned candidate pool to the top 10-20 restaurants to optimize LLM context window and latency.

## Phase 3: LLM Integration (Groq)
**Goal:** Leverage the LLM to rank candidates and generate personalized explanations.

1. **Groq Client Setup**
   - Securely load the Groq API key (via `.env`).
   - Initialize the Groq Python client.
2. **Prompt Engineering**
   - Design a system prompt instructing the LLM on its persona as a restaurant recommender.
   - Create a template to dynamically inject the user's specific context/preferences and the JSON representation of the candidate pool.
3. **Inference & Structured Parsing**
   - Send the prompt to the Groq API.
   - Enforce structured output (JSON schema) from the LLM containing:
     - Ranked list of Restaurant IDs or Names.
     - A 1-2 sentence human-like explanation for each recommendation.
   - Parse the response and merge it with the original restaurant metadata.

## Phase 4: Client / UI Implementation
**Goal:** Build a user-friendly interface to interact with the system.

1. **Frontend Selection & Setup**
   - Use the **React.js + Vite** stack to build the UI, creating a standalone, fast, and modern Single Page Application (SPA).
2. **Input Form**
   - Create form fields for Location, Budget (Low/Med/High), Cuisine, Minimum Rating, and open-text additional preferences.
3. **Results Display**
   - Render the API response clearly, prominently displaying the Restaurant Name, Cuisine, Rating, Estimated Cost, and the **AI-generated explanation**.

## Phase 5: Testing, Tuning & Optimization
**Goal:** Ensure the system is reliable, fast, and provides high-quality recommendations.

1. **End-to-End Testing**
   - Test the complete flow from UI input to LLM output.
   - Handle edge cases (e.g., zero restaurants found in pre-filtering).
2. **Prompt Tuning**
   - Refine the LLM prompt to ensure explanations are natural, concise, and accurately reflect both the user's hidden preferences and the restaurant's actual data.
3. **Latency Optimization**
   - Ensure the pre-filtering step is fast.
   - Verify that the Groq LLM inference completes within acceptable user-facing latency bounds (< 1-2 seconds).
