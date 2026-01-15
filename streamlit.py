"""
Blackcoffer NLP Analysis - Interactive Dashboard

A Streamlit web application for text analysis and visualization.

Run: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os
import subprocess
import time

# Page configuration
st.set_page_config(
    page_title="Blackcoffer NLP Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #667eea;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">📊 Blackcoffer NLP Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=NLP+Analysis", use_column_width=True)
    st.header("⚙️ Control Panel")
    
    page = st.radio(
        "Navigation",
        ["🏠 Home", "📤 Upload & Run", "📊 Results", "📈 Visualizations", "ℹ️ About"]
    )
    
    st.markdown("---")
    st.markdown("### 📋 Quick Stats")
    
    # Check for extracted articles
    extracted_dir = Path("data/raw/extracted_articles")
    if extracted_dir.exists():
        article_count = len(list(extracted_dir.glob("*.txt")))
        st.metric("Articles Extracted", article_count)
    else:
        st.metric("Articles Extracted", 0)
    
    # Check for output file
    output_file = Path("data/output/Output_Data_Structure.xlsx")
    if output_file.exists():
        st.success("✅ Analysis Complete")
    else:
        st.warning("⏳ No results yet")

# HOME PAGE
if page == "🏠 Home":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>🔍</h2>
            <h3>Web Scraping</h3>
            <p>Extract 147+ articles automatically</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>📈</h2>
            <h3>13 Metrics</h3>
            <p>Comprehensive text analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>📊</h2>
            <h3>Visualizations</h3>
            <p>Interactive charts & graphs</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.header("🎯 What This Dashboard Does")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Features")
        st.write("""
        - ✅ Upload Excel files with URLs
        - ✅ Automated web scraping
        - ✅ Real-time progress tracking
        - ✅ Sentiment analysis
        - ✅ Readability metrics
        - ✅ Interactive visualizations
        - ✅ Export results to Excel
        """)
    
    with col2:
        st.subheader("Metrics Calculated")
        st.write("""
        **Sentiment Analysis:**
        - Positive Score
        - Negative Score
        - Polarity Score
        - Subjectivity Score
        
        **Readability:**
        - Avg Sentence Length
        - Complex Words %
        - Fog Index
        - Avg Words/Sentence
        - Complex Word Count
        
        **Word Statistics:**
        - Word Count
        - Syllables/Word
        - Personal Pronouns
        - Avg Word Length
        """)
    
    st.markdown("---")
    st.info("👈 Use the sidebar to navigate to different sections")

# UPLOAD & RUN PAGE
elif page == "📤 Upload & Run":
    st.header("📤 Upload Input File & Run Analysis")
    
    tab1, tab2 = st.tabs(["📁 Upload", "🚀 Run Analysis"])
    
    with tab1:
        st.subheader("Upload Input Excel File")
        
        uploaded_file = st.file_uploader(
            "Choose an Excel file (.xlsx)",
            type=['xlsx'],
            help="Upload your Input.xlsx file containing URLs to scrape"
        )
        
        if uploaded_file is not None:
            # Save the file
            os.makedirs("data/input", exist_ok=True)
            with open("data/input/Input.xlsx", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success("✅ File uploaded successfully!")
            
            # Preview the file
            df = pd.read_excel(uploaded_file)
            st.write(f"**Preview:** {len(df)} URLs found")
            st.dataframe(df.head(10))
    
    with tab2:
        st.subheader("🚀 Run Web Scraper")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Start Web Scraping", key="scrape"):
                with st.spinner("Scraping articles... This may take 15-20 minutes"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # Run scraper
                        result = subprocess.run(
                            ['python', 'scraper.py'],
                            capture_output=True,
                            text=True,
                            timeout=1800
                        )
                        
                        progress_bar.progress(100)
                        
                        if result.returncode == 0:
                            st.success("✅ Scraping completed successfully!")
                            st.text(result.stdout[-500:])  # Show last 500 chars
                        else:
                            st.error("❌ Scraping failed!")
                            st.text(result.stderr)
                    
                    except subprocess.TimeoutExpired:
                        st.error("⏱️ Scraping timed out (>30 minutes)")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        with col2:
            if st.button("📊 Run Text Analysis", key="analyze"):
                with st.spinner("Analyzing articles... This may take 5-10 minutes"):
                    progress_bar = st.progress(0)
                    
                    try:
                        # Run analysis
                        result = subprocess.run(
                            ['python', 'test_analysis.py'],
                            capture_output=True,
                            text=True,
                            timeout=600
                        )
                        
                        progress_bar.progress(100)
                        
                        if result.returncode == 0:
                            st.success("✅ Analysis completed successfully!")
                            st.text(result.stdout[-500:])
                        else:
                            st.error("❌ Analysis failed!")
                            st.text(result.stderr)
                    
                    except subprocess.TimeoutExpired:
                        st.error("⏱️ Analysis timed out (>10 minutes)")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

# RESULTS PAGE
elif page == "📊 Results":
    st.header("📊 Analysis Results")
    
    output_file = Path("data/output/Output_Data_Structure.xlsx")
    
    if output_file.exists():
        df = pd.read_excel(output_file)
        
        # Summary metrics
        st.subheader("📈 Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Articles", len(df))
        with col2:
            avg_polarity = df['POLARITY SCORE'].mean()
            st.metric("Avg Polarity", f"{avg_polarity:.3f}")
        with col3:
            avg_fog = df['FOG INDEX'].mean()
            st.metric("Avg Fog Index", f"{avg_fog:.2f}")
        with col4:
            avg_words = df['WORD COUNT'].mean()
            st.metric("Avg Word Count", f"{int(avg_words)}")
        
        st.markdown("---")
        
        # Filter options
        st.subheader("🔍 Filter Results")
        
        col1, col2 = st.columns(2)
        with col1:
            polarity_filter = st.slider(
                "Polarity Score Range",
                float(df['POLARITY SCORE'].min()),
                float(df['POLARITY SCORE'].max()),
                (float(df['POLARITY SCORE'].min()), float(df['POLARITY SCORE'].max()))
            )
        
        with col2:
            fog_filter = st.slider(
                "Fog Index Range",
                float(df['FOG INDEX'].min()),
                float(df['FOG INDEX'].max()),
                (float(df['FOG INDEX'].min()), float(df['FOG INDEX'].max()))
            )
        
        # Apply filters
        filtered_df = df[
            (df['POLARITY SCORE'] >= polarity_filter[0]) &
            (df['POLARITY SCORE'] <= polarity_filter[1]) &
            (df['FOG INDEX'] >= fog_filter[0]) &
            (df['FOG INDEX'] <= fog_filter[1])
        ]
        
        st.write(f"**Showing {len(filtered_df)} of {len(df)} articles**")
        
        # Display data
        st.dataframe(filtered_df, height=400)
        
        # Download button
        st.download_button(
            label="📥 Download Results (Excel)",
            data=open(output_file, 'rb').read(),
            file_name="Analysis_Results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    else:
        st.warning("⚠️ No results found. Please run the analysis first!")
        st.info("👈 Go to 'Upload & Run' to start the analysis")

# VISUALIZATIONS PAGE
elif page == "📈 Visualizations":
    st.header("📈 Interactive Visualizations")
    
    output_file = Path("data/output/Output_Data_Structure.xlsx")
    
    if output_file.exists():
        df = pd.read_excel(output_file)
        
        # Visualization options
        viz_type = st.selectbox(
            "Select Visualization",
            [
                "Sentiment Distribution",
                "Polarity vs Subjectivity",
                "Readability Analysis",
                "Word Count Distribution",
                "Top Positive Articles",
                "Top Negative Articles",
                "Correlation Heatmap"
            ]
        )
        
        if viz_type == "Sentiment Distribution":
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.histogram(
                    df, 
                    x='POLARITY SCORE',
                    nbins=30,
                    title="Polarity Score Distribution",
                    color_discrete_sequence=['#667eea']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.histogram(
                    df,
                    x='SUBJECTIVITY SCORE',
                    nbins=30,
                    title="Subjectivity Score Distribution",
                    color_discrete_sequence=['#764ba2']
                )
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Polarity vs Subjectivity":
            fig = px.scatter(
                df,
                x='POLARITY SCORE',
                y='SUBJECTIVITY SCORE',
                color='FOG INDEX',
                size='WORD COUNT',
                hover_data=['URL_ID'],
                title="Polarity vs Subjectivity (sized by word count, colored by Fog Index)",
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Readability Analysis":
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.box(
                    df,
                    y='FOG INDEX',
                    title="Fog Index Distribution",
                    color_discrete_sequence=['#667eea']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.box(
                    df,
                    y='AVG SENTENCE LENGTH',
                    title="Average Sentence Length Distribution",
                    color_discrete_sequence=['#764ba2']
                )
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Word Count Distribution":
            fig = px.histogram(
                df,
                x='WORD COUNT',
                nbins=30,
                title="Word Count Distribution",
                color_discrete_sequence=['#667eea']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Top Positive Articles":
            top_positive = df.nlargest(10, 'POSITIVE SCORE')
            fig = px.bar(
                top_positive,
                x='POSITIVE SCORE',
                y='URL_ID',
                orientation='h',
                title="Top 10 Most Positive Articles",
                color='POSITIVE SCORE',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Top Negative Articles":
            top_negative = df.nlargest(10, 'NEGATIVE SCORE')
            fig = px.bar(
                top_negative,
                x='NEGATIVE SCORE',
                y='URL_ID',
                orientation='h',
                title="Top 10 Most Negative Articles",
                color='NEGATIVE SCORE',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Correlation Heatmap":
            # Select numeric columns
            numeric_cols = [
                'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE',
                'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'FOG INDEX',
                'WORD COUNT', 'AVG WORD LENGTH'
            ]
            
            corr_matrix = df[numeric_cols].corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto='.2f',
                aspect='auto',
                color_continuous_scale='RdBu_r',
                title="Correlation Heatmap of Metrics"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("⚠️ No data to visualize. Please run the analysis first!")

# ABOUT PAGE
elif page == "ℹ️ About":
    st.header("ℹ️ About This Dashboard")
    
    st.markdown("""
    ## 📊 Blackcoffer NLP Analysis Dashboard
    
    This interactive dashboard provides a user-friendly interface for performing 
    comprehensive text analysis on articles extracted from URLs.
    
    ### 🎯 Features
    
    - **Web Scraping:** Automatically extract articles from 147+ URLs
    - **Text Analysis:** Calculate 13 comprehensive metrics
    - **Real-time Processing:** Track progress of scraping and analysis
    - **Interactive Visualizations:** Explore data with dynamic charts
    - **Export Results:** Download analysis results in Excel format
    
    ### 📈 Metrics Explained
    
    #### Sentiment Analysis
    - **Positive Score:** Count of positive words in the text
    - **Negative Score:** Count of negative words in the text
    - **Polarity Score:** Overall sentiment (-1 to +1)
    - **Subjectivity Score:** Opinion vs facts (0 to 1)
    
    #### Readability Metrics
    - **Avg Sentence Length:** Average words per sentence
    - **Complex Words %:** Percentage of words with 3+ syllables
    - **Fog Index:** Reading difficulty level (higher = harder)
    - **Avg Words/Sentence:** Same as avg sentence length
    - **Complex Word Count:** Total complex words
    
    #### Word Statistics
    - **Word Count:** Total words (after cleaning)
    - **Syllable/Word:** Average syllables per word
    - **Personal Pronouns:** Count of I, we, my, ours, us
    - **Avg Word Length:** Average characters per word
    
    ### 🛠️ Technology Stack
    
    - **Python:** Core programming language
    - **Streamlit:** Dashboard framework
    - **Plotly:** Interactive visualizations
    - **Pandas:** Data manipulation
    - **NLTK:** Natural language processing
    - **BeautifulSoup:** Web scraping
    
    ### 👨‍💻 Developer
    
    Created for the Blackcoffer Text Analysis Assignment
    
    ### 📚 Documentation
    
    For more information, visit the [GitHub Repository](#)
    """)
    
    st.markdown("---")
    st.success("Made with ❤️ using Streamlit")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Blackcoffer NLP Analysis Dashboard v1.0 | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)