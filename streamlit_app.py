# streamlit_app.py - Creative AI Studio
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import plotly.graph_objects as go
import plotly.express as px
import random
import math
import requests
import json
import io
from PIL import Image
from datetime import datetime, timedelta
import base64

# Page configuration
st.set_page_config(
    page_title="Creative AI Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/creative-ai-studio',
        'Report a bug': "https://github.com/yourusername/creative-ai-studio/issues",
        'About': "# Creative AI Studio\n## All-in-One Art & Data Platform"
    }
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []
if 'saved_projects' not in st.session_state:
    st.session_state.saved_projects = []
if 'current_project' not in st.session_state:
    st.session_state.current_project = {}

# Title and Introduction
st.markdown('<h1 class="main-header">🎨 Creative AI Studio</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">All-in-One Generative Art & Data Visualization Platform</p>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <p>Arts & Advanced Big Data - Final Project | Sungkyunkwan University | Prof. Jahwan Koo</p>
</div>
""", unsafe_allow_html=True)

# Navigation
st.sidebar.title("🚀 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Dashboard", "🎨 Generative Art", "📊 Data Visualization", "🌐 API Explorer", "📁 My Projects", "📚 About"]
)

# Dashboard Page
if page == "🏠 Dashboard":
    st.header("📊 Dashboard")
    
    # Introduction
    st.markdown("""
    ## Welcome to Creative AI Studio!
    
    This platform integrates everything we learned this semester:
    
    - **Generative Art Creation** - Algorithmic art with custom parameters
    - **Data-Driven Design** - Transform CSV data into beautiful visualizations
    - **API Integration** - Connect to external data sources (MET Museum, Weather, Stocks)
    - **Interactive Tools** - Real-time parameter adjustment and preview
    
    ### How to Use:
    1. Select a module from the sidebar
    2. Adjust parameters using the controls
    3. Generate and customize your creations
    4. Save and export your projects
    """)
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Projects Created", len(st.session_state.saved_projects))
    with col2:
        st.metric("Images Generated", len(st.session_state.generated_images))
    with col3:
        st.metric("API Integrations", "3 Active")
    with col4:
        st.metric("Available Styles", "8+")
    
    # Features Grid
    st.header("✨ Key Features")
    
    features = [
        {"icon": "🎨", "title": "Generative Art", "desc": "Create algorithmic art with custom shapes, colors, and patterns"},
        {"icon": "📊", "title": "Data Visualization", "desc": "Transform CSV data into beautiful visual art"},
        {"icon": "🌐", "title": "API Integration", "desc": "Connect to MET Museum, Weather, and Stock APIs"},
        {"icon": "⚡", "title": "Real-time Preview", "desc": "See changes instantly as you adjust parameters"},
        {"icon": "💾", "title": "Project Saving", "desc": "Save and reload your creative projects"},
        {"icon": "📱", "title": "Responsive Design", "desc": "Works on desktop, tablet, and mobile devices"}
    ]
    
    cols = st.columns(3)
    for i, feature in enumerate(features):
        with cols[i % 3]:
            with st.container():
                st.markdown(f"""
                <div class="feature-card">
                    <h3>{feature['icon']} {feature['title']}</h3>
                    <p>{feature['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Quick Start
    st.header("🚀 Quick Start")
    
    quick_cols = st.columns(3)
    with quick_cols[0]:
        if st.button("🎨 Start Generative Art", use_container_width=True):
            st.session_state.page = "🎨 Generative Art"
            st.rerun()
    
    with quick_cols[1]:
        if st.button("📊 Try Data Visualization", use_container_width=True):
            st.session_state.page = "📊 Data Visualization"
            st.rerun()
    
    with quick_cols[2]:
        if st.button("🌐 Explore APIs", use_container_width=True):
            st.session_state.page = "🌐 API Explorer"
            st.rerun()

# Generative Art Page
elif page == "🎨 Generative Art":
    st.header("🎨 Generative Art Studio")
    
    # Import generative art functions
    from generative_art_module import GenerativeArtStudio
    
    studio = GenerativeArtStudio()
    
    # Sidebar controls
    st.sidebar.header("🛠️ Art Controls")
    
    # Style selection
    art_style = st.sidebar.selectbox(
        "Art Style",
        ["Organic Blobs", "Geometric Patterns", "Abstract Lines", "Color Fields", "Noise Art"],
        index=0
    )
    
    # Color palette
    palette = st.sidebar.selectbox(
        "Color Palette",
        ["Pastel", "Vivid", "Monochrome", "Sunset", "Ocean", "Forest", "Custom"],
        index=0
    )
    
    if palette == "Custom":
        col1, col2, col3 = st.sidebar.columns(3)
        with col1:
            color1 = st.color_picker("Color 1", "#FF6B6B")
        with col2:
            color2 = st.color_picker("Color 2", "#4ECDC4")
        with col3:
            color3 = st.color_picker("Color 3", "#45B7D1")
    
    # Parameters
    complexity = st.sidebar.slider("Complexity", 1, 10, 5)
    layers = st.sidebar.slider("Layers", 1, 20, 8)
    randomness = st.sidebar.slider("Randomness", 0.0, 1.0, 0.5)
    
    # Generate button
    if st.sidebar.button("✨ Generate Art", type="primary", use_container_width=True):
        with st.spinner("Creating your masterpiece..."):
            # Generate art based on parameters
            fig = studio.create_art(
                style=art_style,
                palette=palette if palette != "Custom" else [color1, color2, color3],
                complexity=complexity,
                layers=layers,
                randomness=randomness
            )
            
            # Display the art
            st.pyplot(fig)
            
            # Save to session state
            art_data = {
                "style": art_style,
                "palette": palette,
                "complexity": complexity,
                "layers": layers,
                "randomness": randomness,
                "timestamp": datetime.now().isoformat()
            }
            st.session_state.generated_images.append(art_data)
            
            # Save options
            col1, col2 = st.columns(2)
            with col1:
                buf = io.BytesIO()
                fig.savefig(buf, format="png", dpi=300)
                buf.seek(0)
                st.download_button(
                    label="💾 Download PNG",
                    data=buf,
                    file_name=f"generative_art_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png",
                    use_container_width=True
                )
            with col2:
                if st.button("📁 Save Project", use_container_width=True):
                    st.session_state.saved_projects.append(art_data)
                    st.success("Project saved!")

# Data Visualization Page
elif page == "📊 Data Visualization":
    st.header("📊 Data Visualization Studio")
    
    # Import data visualization functions
    from data_viz_module import DataVisualizer
    
    viz = DataVisualizer()
    
    # Data upload section
    st.subheader("📁 Upload Your Data")
    
    upload_option = st.radio(
        "Data Source",
        ["Upload CSV File", "Use Sample Data", "Generate Random Data"],
        horizontal=True
    )
    
    data = None
    
    if upload_option == "Upload CSV File":
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            st.success(f"Successfully loaded {len(data)} rows")
    
    elif upload_option == "Use Sample Data":
        # Load sample data
        sample_data = {
            'Category': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
            'Value1': [25, 34, 22, 45, 38, 28, 32, 40],
            'Value2': [45, 28, 35, 42, 30, 48, 25, 38],
            'Value3': [18, 22, 30, 25, 42, 20, 35, 28],
            'Growth': [0.1, 0.25, -0.05, 0.33, 0.17, -0.12, 0.28, 0.15]
        }
        data = pd.DataFrame(sample_data)
        st.info("Using sample data")
    
    else:  # Generate Random Data
        num_points = st.slider("Number of data points", 10, 100, 50)
        data = pd.DataFrame({
            'x': np.random.randn(num_points),
            'y': np.random.randn(num_points),
            'size': np.random.uniform(10, 100, num_points),
            'category': np.random.choice(['A', 'B', 'C', 'D'], num_points)
        })
    
    if data is not None:
        st.subheader("📈 Data Preview")
        st.dataframe(data.head(), use_container_width=True)
        
        # Visualization options
        st.subheader("🎨 Visualization Options")
        
        viz_type = st.selectbox(
            "Visualization Type",
            ["Scatter Plot", "Bar Chart", "Line Chart", "Heatmap", "Pie Chart", "Radar Chart"]
        )
        
        if viz_type == "Scatter Plot":
            col1, col2, col3 = st.columns(3)
            with col1:
                x_col = st.selectbox("X Axis", data.columns.tolist())
            with col2:
                y_col = st.selectbox("Y Axis", data.columns.tolist())
            with col3:
                color_col = st.selectbox("Color By", ["None"] + data.columns.tolist())
            
            fig = px.scatter(data, x=x_col, y=y_col, color=color_col if color_col != "None" else None)
        
        elif viz_type == "Bar Chart":
            x_col = st.selectbox("Category Column", data.columns.tolist())
            y_col = st.selectbox("Value Column", data.columns.tolist())
            fig = px.bar(data, x=x_col, y=y_col)
        
        # Display the visualization
        st.plotly_chart(fig, use_container_width=True)

# API Explorer Page
elif page == "🌐 API Explorer":
    st.header("🌐 API Explorer Hub")
    
    api_choice = st.selectbox(
        "Choose API to Explore",
        ["MET Museum Art Collection", "Open-Meteo Weather", "Stock Market Data", "News API"]
    )
    
    if api_choice == "MET Museum Art Collection":
        st.subheader("🏛️ MET Museum Art Explorer")
        
        search_term = st.text_input("Search for artworks:", "flower")
        
        if st.button("Search Artworks"):
            with st.spinner("Searching MET Museum collection..."):
                # MET API integration
                search_url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
                params = {'q': search_term, 'hasImages': True}
                
                try:
                    response = requests.get(search_url, params=params)
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"Found {data.get('total', 0)} artworks")
                        
                        # Display first few results
                        if data.get('objectIDs'):
                            for obj_id in data['objectIDs'][:5]:
                                details_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}"
                                details_response = requests.get(details_url)
                                if details_response.status_code == 200:
                                    artwork = details_response.json()
                                    if artwork.get('primaryImage'):
                                        col1, col2 = st.columns([1, 2])
                                        with col1:
                                            st.image(artwork['primaryImage'], use_column_width=True)
                                        with col2:
                                            st.write(f"**{artwork.get('title', 'Unknown')}**")
                                            st.write(f"Artist: {artwork.get('artistDisplayName', 'Unknown')}")
                                            st.write(f"Date: {artwork.get('objectDate', 'Unknown')}")
                                            st.write(f"Department: {artwork.get('department', 'Unknown')}")
                                        st.markdown("---")
                except Exception as e:
                    st.error(f"Error accessing MET API: {e}")
    
    elif api_choice == "Open-Meteo Weather":
        st.subheader("🌤️ Weather Data Explorer")
        
        # Simple weather display
        cities = {
            "Seoul": (37.5665, 126.9780),
            "Tokyo": (35.6762, 139.6503),
            "New York": (40.7128, -74.0060),
            "London": (51.5074, -0.1278),
            "Sydney": (-33.8688, 151.2093)
        }
        
        selected_city = st.selectbox("Select City", list(cities.keys()))
        
        if st.button("Get Weather"):
            lat, lon = cities[selected_city]
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    weather = response.json()['current_weather']
                    temp = weather['temperature']
                    windspeed = weather['windspeed']
                    weathercode = weather['weathercode']
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Temperature", f"{temp}°C")
                    with col2:
                        st.metric("Wind Speed", f"{windspeed} km/h")
                    with col3:
                        st.metric("Weather Code", weathercode)
                    
                    # Simple weather interpretation
                    if weathercode == 0:
                        st.success("Clear sky ☀️")
                    elif weathercode in [1, 2, 3]:
                        st.info("Partly cloudy ⛅")
                    elif weathercode in [45, 48]:
                        st.warning("Foggy 🌫️")
                    elif weathercode in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
                        st.warning("Rainy 🌧️")
                    elif weathercode in [95, 96, 99]:
                        st.error("Thunderstorm ⛈️")
            except Exception as e:
                st.error(f"Error accessing weather API: {e}")

# My Projects Page
elif page == "📁 My Projects":
    st.header("📁 My Saved Projects")
    
    if not st.session_state.saved_projects:
        st.info("You haven't saved any projects yet. Create something amazing in the other sections!")
    else:
        for i, project in enumerate(st.session_state.saved_projects):
            with st.expander(f"Project {i+1}: {project.get('style', 'Unknown')} - {project.get('timestamp', '')}"):
                st.json(project)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Load Project {i+1}", key=f"load_{i}"):
                        st.session_state.current_project = project
                        st.success("Project loaded! Go to the appropriate section to view it.")
                with col2:
                    if st.button(f"Delete Project {i+1}", key=f"delete_{i}"):
                        st.session_state.saved_projects.pop(i)
                        st.rerun()

# About Page
elif page == "📚 About":
    st.header("📚 About Creative AI Studio")
    
    st.markdown("""
    ## Final Project: Arts & Advanced Big Data
    
    **Student:** [Your Name]
    **Course:** Arts and Advanced Big Data
    **Instructor:** Prof. Jahwan Koo
    **University:** Sungkyunkwan University
    **Semester:** 2025 Fall
    
    ### Project Overview
    
    Creative AI Studio is an all-in-one platform that integrates everything learned during the semester:
    
    1. **Generative Art Creation** - Algorithmic art generation using mathematical functions
    2. **Data Visualization** - Transforming structured data into artistic representations
    3. **API Integration** - Connecting to external data sources and services
    4. **Interactive Web Application** - Real-time parameter adjustment and preview
    
    ### Technical Implementation
    
    - **Frontend:** Streamlit for web interface
    - **Visualization:** Matplotlib, Plotly for charts and graphics
    - **Data Processing:** Pandas, NumPy
    - **API Integration:** Requests library
    - **Deployment:** Streamlit Cloud
    
    ### Learning Outcomes
    
    This project demonstrates proficiency in:
    - Prompt-based coding with AI assistance
    - Data-driven design and visualization
    - Web application development
    - API integration and data fetching
    - Creative coding and algorithmic art
    
    ### Source Code
    
    The complete source code is available on GitHub:
    [https://github.com/yourusername/creative-ai-studio](https://github.com/yourusername/creative-ai-studio)
    
    ### Live Demo
    
    Access the live application at:
    [https://your-app-name.streamlit.app](https://your-app-name.streamlit.app)
    """)
    
    # Course progress visualization
    st.subheader("📈 Course Progress")
    
    weeks = [f"Week {i}" for i in range(1, 11)]
    topics = [
        "Course Introduction",
        "Coding with Prompt",
        "Practice Session",
        "Interactive & 3D",
        "Data-Driven (CSV)",
        "Chuseok Break",
        "MCP Protocol",
        "Mid-Term",
        "Web-based",
        "Open API"
    ]
    completion = [100, 100, 100, 100, 100, 0, 80, 100, 100, 100]
    
    progress_df = pd.DataFrame({
        "Week": weeks,
        "Topic": topics,
        "Completion": completion
    })
    
    fig = px.bar(progress_df, x="Week", y="Completion", 
                 color="Completion", color_continuous_scale="Viridis",
                 title="Course Topics Covered")
    st.plotly_chart(fig, use_container_width=True)

# Helper modules (simplified versions - in real project these would be separate files)
class GenerativeArtStudio:
    def __init__(self):
        pass
    
    def create_art(self, style, palette, complexity, layers, randomness):
        """Generate generative art based on parameters"""
        fig, ax = plt.subplots(figsize=(10, 10))
        
        if style == "Organic Blobs":
            self._create_organic_blobs(ax, palette, complexity, layers, randomness)
        elif style == "Geometric Patterns":
            self._create_geometric_patterns(ax, palette, complexity, layers)
        
        ax.set_aspect('equal')
        ax.axis('off')
        plt.tight_layout()
        return fig
    
    def _create_organic_blobs(self, ax, palette, complexity, layers, randomness):
        """Create organic blob shapes"""
        for _ in range(layers):
            center = (random.random(), random.random())
            radius = random.random() * 0.2 + 0.1
            
            # Generate blob shape
            angles = np.linspace(0, 2 * math.pi, 100)
            radii = radius * (1 + randomness * np.random.randn(100) * 0.3)
            radii = np.maximum(radii, radius * 0.3)
            
            x = center[0] + radii * np.cos(angles)
            y = center[1] + radii * np.sin(angles)
            
            # Choose color based on palette
            if palette == "Pastel":
                color = (random.random() * 0.5 + 0.5, 
                         random.random() * 0.5 + 0.5, 
                         random.random() * 0.5 + 0.5)
            elif palette == "Vivid":
                color = (random.random(), random.random(), random.random())
            else:  # Monochrome
                base = random.random() * 0.5 + 0.3
                color = (base, base, base)
            
            polygon = Polygon(np.column_stack([x, y]), 
                             facecolor=color, alpha=0.7, edgecolor='none')
            ax.add_patch(polygon)

class DataVisualizer:
    def __init__(self):
        pass

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>🎨 Creative AI Studio | Final Project | Arts & Advanced Big Data</p>
    <p>Sungkyunkwan University | Prof. Jahwan Koo | Fall 2025</p>
    <p>Built with Streamlit • Deployed on Streamlit Cloud</p>
    </div>
    """,
    unsafe_allow_html=True
)
