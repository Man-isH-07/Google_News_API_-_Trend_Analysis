import streamlit as st
import requests
import time

# FastAPI URL
API_URL = "http://127.0.0.1:8000"

# Streamlit page config
st.set_page_config(page_title="News Trends App", layout="wide")

# Enhanced CSS for news website look with animations
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        font-family: Arial, sans-serif;
    }
    h1 {
        color: #2c3e50;
        font-size: 36px;
        margin-bottom: 20px;
        text-align: center;
        animation: fadeIn 1s ease-in;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 0;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        margin: 5px 0;
        padding: 8px 16px;
        border-radius: 5px;
        border: none;
        width: 100%;
        transition: transform 0.3s, background-color 0.3s;
        cursor: pointer;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
    .stButton>button:nth-child(1) { background-color: #4CAF50; color: white; } /* Top News (Green) */
    .stButton>button:nth-child(2) { background-color: #ff9800; color: white; } /* Topic News (Orange) */
    .stButton>button:nth-child(3) { background-color: #2196F3; color: white; } /* Update Trends (Blue) */
    .stButton>button:nth-child(4) { background-color: #f44336; color: white; } /* Test API Root (Red) */
    .stButton>button:nth-child(5) { background-color: #4CAF50; color: white; } /* Start Exploring (Green) */
    hr {
        border: 1px solid #ccc;
        margin: 5px 0;
    }
    .news-article {
        padding: 15px;
        background-color: #f9f9f9;
        border-radius: 5px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        animation: slideIn 0.8s ease-out;
    }
    .welcome-message, .waiting-message {
        text-align: center;
        font-size: 24px;
        color: #2c3e50;
        animation: fadeIn 1s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideIn {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    .stTextInput>label {
        font-weight: bold;
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("News Trends Explorer")

# Function to call API and handle errors with animation delay
def call_api(endpoint, params=None):
    try:
        url = f"{API_URL}{endpoint}"
        if params:
            url += "?" + "&".join(f"{k}={v}" for k, v in params.items() if v)
        time.sleep(0.5)  # Small delay for animation effect
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

# Initialize session state to track if welcome has been shown and if a request has been made
if 'welcome_shown' not in st.session_state:
    st.session_state.welcome_shown = False
if 'request_made' not in st.session_state:
    st.session_state.request_made = False

# Sidebar for welcome and actions
with st.sidebar:
    if not st.session_state.welcome_shown:
        st.markdown('<div class="welcome-message">Welcome to News Trends Explorer!</div>', unsafe_allow_html=True)
        if st.button("Start Exploring"):
            st.session_state.welcome_shown = True
            st.rerun()  # Rerun the app to show the controls
    else:
        st.header("Options")
        
        # Region selection with dropdowns
        LANGUAGES = ["en", "hi", "es", "fr", "uk", "ja"]
        COUNTRIES = ["WORLD", "US", "IN", "GB", "MX", "UA", "JP"]
        
        lang = st.selectbox("Language", LANGUAGES, index=0)  # Default to "en"
        country = st.selectbox("Country", COUNTRIES, index=0)  # Default to "WORLD"
        
        # Action buttons with different colors and horizontal lines
        st.subheader("Actions")

        st.markdown(
            """<hr style="margin:5px 0; border:1px solid #ccc;">""",
            unsafe_allow_html=True,
        )
        fetch_top = st.button("Top News")

        st.markdown(
            """<hr style="margin:5px 0; border:1px solid #ccc;">""",
            unsafe_allow_html=True,
        )
        topic = st.text_input("Enter Topic (e.g., 'technology')", "")
        fetch_topic = st.button("Topic News")

        st.markdown(
            """<hr style="margin:5px 0; border:1px solid #ccc;">""",
            unsafe_allow_html=True,
        )
        update_trends = st.button("Update Trends")

        st.markdown(
            """<hr style="margin:5px 0; border:1px solid #ccc;">""",
            unsafe_allow_html=True,
        )
        test_root = st.button("Test API Root")

# Main content (left) for results
st.header("Results")

# Show welcome or waiting message in main area, fetch news only on button click
if not st.session_state.welcome_shown:
    st.markdown('<div class="welcome-message">Welcome to News Trends Explorer! Click "Start Exploring" in the sidebar to begin.</div>', unsafe_allow_html=True)
else:
    if not st.session_state.request_made:
        st.markdown('<div class="waiting-message">Waiting for Request...</div>', unsafe_allow_html=True)
    
    # Handle user interactions (fetch news only when buttons are clicked)
    if fetch_top:
        params = {"lang": lang, "country": country, "limit": 10}
        result = call_api("/fetch_trends", params)
        if result:
            st.session_state.request_made = True  # Mark that a request has been made
            st.subheader(result["feed_title"])
            for article in result["articles"]:
                with st.container():
                    st.markdown(f'<div class="news-article"><h3>{article["title"]}</h3><p><strong>Source:</strong> <a href="{article["link"]}" target="_blank">{article["source"]}</a></p><p><strong>Published:</strong> {article["published"]}</p></div>', unsafe_allow_html=True)
                st.write("---")  # Horizontal line after each article

        st.write("---")  # Horizontal line after Top News section

    elif fetch_topic and topic:  # Only fetch if topic is not empty
        params = {"lang": lang, "country": country, "limit": 10}
        result = call_api(f"/fetch_trends/{topic}", params)
        if result:
            st.session_state.request_made = True  # Mark that a request has been made
            st.write("### Enter Topic")
            st.write(f"Topic: {topic}")
            st.subheader(result["feed_title"])
            for article in result["articles"]:
                with st.container():
                    st.markdown(f'<div class="news-article"><h3>{article["title"]}</h3><p><strong>Source:</strong> <a href="{article["link"]}" target="_blank">{article["source"]}</a></p><p><strong>Published:</strong> {article["published"]}</p></div>', unsafe_allow_html=True)
                st.write("---")  # Horizontal line after each article

        st.write("---")  # Horizontal line after Topic News section

    elif update_trends:
        params = {"lang": lang, "country": country}
        result = call_api("/update_trends", params)
        if result:
            st.session_state.request_made = True  # Mark that a request has been made
            st.write(result)
        st.write("---")  # Horizontal line after Update Trends

    elif test_root:
        result = call_api("/")
        if result:
            st.session_state.request_made = True  # Mark that a request has been made
            st.write(result)
        st.write("---")  # Horizontal line after Test API Root

# Footer
st.markdown("---")
st.write("Built with Streamlit & FastAPI | News from Google News")