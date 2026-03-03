import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime

# Add root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.phase_1_data.dataset_loader import ZomatoLoader
from app.phase_3_search.search_engine import RestaurantSearchEngine
from app.phase_4_llm.groq_client import GroqRecommendationClient

# Page Config
st.set_page_config(
    page_title="Zomato AI Recommendation",
    page_icon="🍴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #e03a3a;
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
    }
    .resto-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border-left: 5px solid #ff4b4b;
    }
    .resto-name {
        color: #2d3436;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .resto-meta {
        color: #636e72;
        font-size: 0.9rem;
    }
    .rating-badge {
        background-color: #2ecc71;
        color: white;
        padding: 2px 8px;
        border-radius: 5px;
        font-weight: bold;
    }
    .ai-summary-box {
        background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Components
@st.cache_resource
def get_components():
    loader = ZomatoLoader()
    df = loader.get_structured_data()
    search_engine = RestaurantSearchEngine()
    llm_client = GroqRecommendationClient()
    return df, search_engine, llm_client

df, search_engine, llm_client = get_components()

# Sidebar Inputs
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/b/bd/Zomato_Logo.png", width=200)
    st.title("Filters")
    
    locations = sorted(df["location"].dropna().unique().tolist())
    selected_location = st.selectbox("Select Location", options=[""] + locations, index=0)
    
    max_price = st.slider("Max Budget for Two (₹)", min_value=100, max_value=10000, value=1000, step=100)
    
    limit = st.number_input("Number of Recommendations", min_value=3, max_value=20, value=10)
    
    search_clicked = st.button("Find My Next Meal 🚀")

# Main Content
st.title("🍴 Zomato AI Concierge")
st.markdown("Discover the best dining spots tailored for you, enhanced with AI insights.")

if search_clicked:
    if not selected_location:
        st.warning("Please select a location first!")
    else:
        with st.spinner(f"Searching in {selected_location}..."):
            results_df = search_engine.search(df, selected_location, max_price, limit)
            
            if results_df.empty:
                st.info("No restaurants found matching your criteria. Try adjusting your budget or location.")
            else:
                # AI Summary Layer
                st.subheader("🤖 AI Culinary Insight")
                with st.spinner("Groq is analyzing the matches..."):
                    ai_data = llm_client.generate_summary(results_df)
                    overall_summary = ai_data.get("overall_summary", "AI summary unavailable.")
                    individual_summaries = ai_data.get("individual_summaries", {})
                    
                    if "QUOTA_EXCEEDED" in overall_summary:
                        st.warning("⏱️ **AI Summary is taking a breather.** You've reached the free tier limit for Groq API. Please wait about a minute and try again!")
                    else:
                        st.markdown(f"""
                            <div class="ai-summary-box">
                                {overall_summary}
                            </div>
                        """, unsafe_allow_html=True)
                
                # Results Grid
                st.subheader(f"Top {len(results_df)} Picks in {selected_location}")
                
                # Display Results in Cards
                for _, row in results_df.iterrows():
                    resto_name = row['name']
                    insight = individual_summaries.get(resto_name, "")
                    insight_html = f'<div style="margin-top: 10px; font-style: italic; color: #ff4b4b; font-size: 0.85rem;">✨ <b>Insight:</b> {insight}</div>' if insight else ""
                    
                    st.markdown(f"""
                        <div class="resto-card">
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <div class="resto-name">{resto_name}</div>
                                <div class="rating-badge">⭐ {row['rate']}</div>
                            </div>
                            <div class="resto-meta">
                                <b>Cuisines:</b> {row['cuisines']}<br>
                                <b>Cost for 2:</b> ₹{row['approx_cost(for two people)']}
                                {insight_html}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

else:
    # Welcome State
    st.info("👈 Use the sidebar to set your preferences and get started!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Restaurants", f"{len(df):,}")
    with col2:
        st.metric("Unique Locations", f"{len(df['location'].unique()):,}")
    with col3:
        st.metric("Cuisine Types", f"{len(df['cuisines'].dropna().unique()):,}")

# Footer
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: grey;'>Built with ❤️ using Streamlit & Gemini AI • {datetime.now().year}</p>", unsafe_allow_html=True)
