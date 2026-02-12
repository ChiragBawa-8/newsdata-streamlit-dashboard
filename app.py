import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from collections import Counter
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="NewsData.io Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stProgress > div > div > div > div {
        background-color: #667eea;
    }
    h1 {
        color: #667eea;
        text-align: center;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📊 NewsData.io Analysis Dashboard")
st.markdown("### Advanced News Analytics with Sentiment Analysis & Visualizations")

# Initialize session state
if 'articles' not in st.session_state:
    st.session_state.articles = []
if 'total_results' not in st.session_state:
    st.session_state.total_results = 0
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'api_url' not in st.session_state:
    st.session_state.api_url = ""
if 'api_params' not in st.session_state:
    st.session_state.api_params = {}

# Sidebar - API Configuration
st.sidebar.header("🔑 API Configuration")
api_key = st.sidebar.text_input("API Key", type="password", help="Enter your NewsData.io API key")

# Sidebar - Endpoint Selection
st.sidebar.header("🎯 Select Endpoint")
endpoint = st.sidebar.radio(
    "Endpoint Type",
    ["Latest News", "Crypto News", "Archive News"],
    help="Choose which NewsData.io endpoint to use"
)

# Sidebar - Filters
st.sidebar.header("🔍 Search & Filters")

# Search filters
search_query = st.sidebar.text_input("Search Query (q)", help="Search anywhere in article")
search_title = st.sidebar.text_input("Search in Title (qInTitle)", help="Search only in titles")

# Geographic filters
col1, col2 = st.sidebar.columns(2)
with col1:
    country = st.text_input("Country", help="e.g., us, gb, in")
with col2:
    language = st.selectbox("Language", ["", "en", "es", "fr", "de", "it", "pt", "ar", "zh", "ja", "hi"])

# Content filters
category = st.sidebar.selectbox(
    "Category",
    ["", "business", "entertainment", "environment", "food", "health", 
     "politics", "science", "sports", "technology", "top", "world"]
)

sentiment_filter = st.sidebar.selectbox("Sentiment", ["", "positive", "neutral", "negative"])
domain = st.sidebar.text_input("Domain", help="e.g., bbc.com")

# Crypto-specific filter
if endpoint == "Crypto News":
    coin = st.sidebar.text_input("Coin (comma-separated)", help="e.g., btc, eth, sol")

# Time range selection
st.sidebar.header("⏰ Time Range")

if endpoint in ["Latest News", "Crypto News"]:
    time_range_type = st.sidebar.radio("Time Range Type", ["Hours", "Minutes"])
    
    if time_range_type == "Hours":
        time_value = st.sidebar.slider("Hours", 1, 48, 24)
    else:
        time_value = st.sidebar.slider("Minutes", 1, 2880, 1440)
else:  # Archive
    col1, col2 = st.sidebar.columns(2)
    with col1:
        from_date = st.date_input(
            "From Date",
            value=datetime.now() - timedelta(days=30),
            min_value=datetime.now() - timedelta(days=7*365),
            max_value=datetime.now()
        )
    with col2:
        to_date = st.date_input(
            "To Date",
            value=datetime.now(),
            min_value=datetime.now() - timedelta(days=7*365),
            max_value=datetime.now()
        )

# Reset button
if st.sidebar.button("🔄 Reset All Filters"):
    st.session_state.articles = []
    st.session_state.total_results = 0
    st.session_state.analysis_done = False
    st.rerun()


def build_api_url(api_key, endpoint_type, next_page=None):
    """Build API URL with parameters"""
    base_urls = {
        "Latest News": "https://local.newsdata.io/api/1/latest",
        "Crypto News": "https://local.newsdata.io/api/1/crypto",
        "Archive News": "https://local.newsdata.io/api/1/archive"
    }
    
    url = base_urls[endpoint_type]
    params = {"apikey": api_key}
    
    # Add filters
    if search_query:
        params["q"] = search_query
    if search_title:
        params["qInTitle"] = search_title
    if country:
        params["country"] = country
    if language:
        params["language"] = language
    if category:
        params["category"] = category
    if sentiment_filter:
        params["sentiment"] = sentiment_filter
    if domain:
        params["domain"] = domain
    
    # Crypto specific
    if endpoint_type == "Crypto News" and 'coin' in locals() and coin:
        params["coin"] = coin
    
    # Time range
    if endpoint_type in ["Latest News", "Crypto News"]:
        params["timeframe"] = time_value
    else:  # Archive
        params["from_date"] = from_date.strftime("%Y-%m-%d")
        params["to_date"] = to_date.strftime("%Y-%m-%d")
    
    # Pagination
    if next_page:
        params["page"] = next_page
    
    # Store in session state (without API key for display)
    display_params = {k: v for k, v in params.items() if k != 'apikey'}
    st.session_state.api_url = url
    st.session_state.api_params = display_params
    
    return url, params


def clean_keywords(keywords):
    """Clean keywords by removing null values"""
    if not keywords:
        return []
    
    cleaned = []
    for kw in keywords:
        if kw and kw != 'null' and str(kw).lower() != 'null':
            cleaned.append(str(kw).strip().lower())
    
    return cleaned


def fetch_all_news(api_key, endpoint_type, progress_bar, status_text):
    """Fetch all news articles with pagination"""
    articles = []
    next_page = None
    page_count = 0
    max_pages = 50
    
    while page_count < max_pages:
        page_count += 1
        
        try:
            url, params = build_api_url(api_key, endpoint_type, next_page)
            response = requests.get(url, params=params, timeout=30)
            
            # Rate limit check
            if response.status_code == 429:
                st.error("⚠️ Rate limit reached! Showing results from fetched articles.")
                break
            
            data = response.json()
            
            if data.get("status") == "error":
                st.error(f"API Error: {data.get('results', {}).get('message', 'Unknown error')}")
                break
            
            results = data.get("results", [])
            if results:
                articles.extend(results)
            
            # Update progress
            progress = min(page_count / max_pages, 1.0)
            progress_bar.progress(progress)
            status_text.text(f"Pages Fetched: {page_count} | Articles: {len(articles):,}")
            
            next_page = data.get("nextPage")
            
            if not next_page:
                break
            
            # Delay for archive endpoint
            if endpoint_type == "Archive News":
                time.sleep(1)
        
        except Exception as e:
            st.error(f"Fetch Error: {str(e)}. Showing partial results.")
            break
    
    status_text.text(f"✓ Complete! Pages: {page_count} | Articles: {len(articles):,}")
    progress_bar.progress(1.0)
    
    return articles


def generate_stats(articles):
    """Generate statistics cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    unique_sources = len(set([a.get('source_id') for a in articles if a.get('source_id')]))
    
    avg_positive = 0
    valid_count = 0
    for a in articles:
        if a.get('sentiment_stats'):
            avg_positive += a['sentiment_stats'].get('positive', 0)
            valid_count += 1
    avg_positive = avg_positive / valid_count if valid_count > 0 else 0
    
    countries = []
    for a in articles:
        if a.get('country'):
            countries.extend(a['country'])
    unique_countries = len(set([c for c in countries if c]))
    
    with col1:
        st.metric("📰 Articles Analyzed", f"{len(articles):,}")
    with col2:
        st.metric("📡 Unique Sources", unique_sources)
    with col3:
        st.metric("😊 Avg Positive Sentiment", f"{avg_positive:.1f}%")
    with col4:
        st.metric("🌍 Countries Covered", unique_countries)


def plot_source_chart(articles):
    """Plot news by source"""
    source_counts = Counter([a.get('source_name', 'Unknown') for a in articles])
    top_sources = dict(source_counts.most_common(10))
    
    fig = px.bar(
        x=list(top_sources.values()),
        y=list(top_sources.keys()),
        orientation='h',
        title="📰 News by Source (Top 10)",
        labels={'x': 'Number of Articles', 'y': 'Source'},
        color_discrete_sequence=['#667eea']
    )
    fig.update_layout(height=400, showlegend=False)
    
    return fig


def plot_sentiment_chart(articles):
    """Plot sentiment distribution"""
    sentiment_counts = Counter([a.get('sentiment', 'neutral') for a in articles])
    
    fig = px.pie(
        values=list(sentiment_counts.values()),
        names=list(sentiment_counts.keys()),
        title="😊 Sentiment Distribution",
        color_discrete_sequence=['#4bc0c0', '#ffce56', '#ff6384']
    )
    fig.update_layout(height=400)
    
    return fig


def plot_category_chart(articles):
    """Plot category distribution"""
    categories = []
    for a in articles:
        if a.get('category'):
            categories.extend(a['category'])
    
    category_counts = Counter(categories)
    top_categories = dict(category_counts.most_common(8))
    
    fig = px.pie(
        values=list(top_categories.values()),
        names=list(top_categories.keys()),
        title="📁 Category Distribution",
        hole=0.3
    )
    fig.update_layout(height=400)
    
    return fig


def plot_country_chart(articles):
    """Plot country distribution"""
    countries = []
    for a in articles:
        if a.get('country'):
            countries.extend([c.upper() for c in a['country'] if c])
    
    country_counts = Counter(countries)
    top_countries = dict(country_counts.most_common(10))
    
    fig = px.bar(
        x=list(top_countries.values()),
        y=list(top_countries.keys()),
        orientation='h',
        title="🌍 Country Distribution",
        labels={'x': 'Number of Articles', 'y': 'Country'},
        color_discrete_sequence=['#9966ff']
    )
    fig.update_layout(height=400, showlegend=False)
    
    return fig


def plot_sentiment_scores(articles):
    """Plot average sentiment scores"""
    avg_scores = {'positive': 0, 'neutral': 0, 'negative': 0}
    valid_count = 0
    
    for a in articles:
        if a.get('sentiment_stats'):
            avg_scores['positive'] += a['sentiment_stats'].get('positive', 0)
            avg_scores['neutral'] += a['sentiment_stats'].get('neutral', 0)
            avg_scores['negative'] += a['sentiment_stats'].get('negative', 0)
            valid_count += 1
    
    if valid_count > 0:
        for key in avg_scores:
            avg_scores[key] /= valid_count
    
    fig = px.bar(
        x=['Positive', 'Neutral', 'Negative'],
        y=[avg_scores['positive'], avg_scores['neutral'], avg_scores['negative']],
        title="📊 Average Sentiment Scores (%)",
        labels={'x': 'Sentiment', 'y': 'Average Score (%)'},
        color=['Positive', 'Neutral', 'Negative'],
        color_discrete_map={'Positive': '#4bc0c0', 'Neutral': '#ffce56', 'Negative': '#ff6384'}
    )
    fig.update_layout(height=400, showlegend=False)
    
    return fig


def plot_timeline(articles):
    """Plot articles over time"""
    dates = []
    for a in articles:
        if a.get('pubDate'):
            date_str = a['pubDate'].split(' ')[0]
            dates.append(date_str)
    
    date_counts = Counter(dates)
    sorted_dates = sorted(date_counts.items())
    
    if not sorted_dates:
        return None
    
    df = pd.DataFrame(sorted_dates, columns=['Date', 'Count'])
    
    fig = px.line(
        df,
        x='Date',
        y='Count',
        title="📅 Articles Over Time",
        labels={'Count': 'Number of Articles'},
        markers=True
    )
    fig.update_traces(line_color='#667eea', fill='tozeroy', fillcolor='rgba(102, 126, 234, 0.2)')
    fig.update_layout(height=400)
    
    return fig


def generate_wordcloud(articles):
    """Generate word cloud from keywords"""
    all_keywords = []
    for a in articles:
        if a.get('keywords'):
            cleaned = clean_keywords(a['keywords'])
            all_keywords.extend(cleaned)
    
    if not all_keywords:
        return None
    
    # Count keywords
    keyword_counts = Counter(all_keywords)
    
    # Filter out single occurrences
    filtered_keywords = {k: v for k, v in keyword_counts.items() if v > 1}
    
    if not filtered_keywords:
        return None
    
    # Generate word cloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        relative_scaling=0.5,
        min_font_size=10
    ).generate_from_frequencies(filtered_keywords)
    
    return wordcloud


def get_sentiment_summary(articles):
    """Get detailed sentiment summary"""
    sentiment_data = {
        'positive': [],
        'neutral': [],
        'negative': []
    }
    
    for article in articles:
        if article.get('sentiment_stats'):
            sentiment_data['positive'].append(article['sentiment_stats'].get('positive', 0))
            sentiment_data['neutral'].append(article['sentiment_stats'].get('neutral', 0))
            sentiment_data['negative'].append(article['sentiment_stats'].get('negative', 0))
    
    if not sentiment_data['positive']:
        return None
    
    summary = {
        'avg_positive': sum(sentiment_data['positive']) / len(sentiment_data['positive']),
        'avg_neutral': sum(sentiment_data['neutral']) / len(sentiment_data['neutral']),
        'avg_negative': sum(sentiment_data['negative']) / len(sentiment_data['negative']),
        'max_positive': max(sentiment_data['positive']),
        'max_negative': max(sentiment_data['negative']),
        'min_positive': min(sentiment_data['positive']),
        'min_negative': min(sentiment_data['negative'])
    }
    
    return summary


def export_to_pdf(articles, sentiment_summary):
    """Export analysis results to PDF"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    
    # Container for PDF elements
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph("NewsData.io Analysis Report", title_style)
    elements.append(title)
    
    # Date
    date_text = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
    elements.append(date_text)
    elements.append(Spacer(1, 20))
    
    # API URL Information
    elements.append(Paragraph("API Request Details", heading_style))
    api_info = f"<b>Endpoint:</b> {st.session_state.api_url}<br/>"
    api_info += "<b>Parameters:</b><br/>"
    for key, value in st.session_state.api_params.items():
        api_info += f"&nbsp;&nbsp;&nbsp;&nbsp;• {key}: {value}<br/>"
    elements.append(Paragraph(api_info, styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Summary Statistics
    elements.append(Paragraph("Summary Statistics", heading_style))
    
    unique_sources = len(set([a.get('source_id') for a in articles if a.get('source_id')]))
    countries = []
    for a in articles:
        if a.get('country'):
            countries.extend(a['country'])
    unique_countries = len(set([c for c in countries if c]))
    
    stats_data = [
        ['Metric', 'Value'],
        ['Total Articles Analyzed', f"{len(articles):,}"],
        ['Unique Sources', str(unique_sources)],
        ['Countries Covered', str(unique_countries)],
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 20))
    
    # Sentiment Analysis Results
    if sentiment_summary:
        elements.append(Paragraph("Sentiment Analysis Results", heading_style))
        
        sentiment_data = [
            ['Sentiment Type', 'Average (%)', 'Maximum (%)', 'Minimum (%)'],
            ['Positive', f"{sentiment_summary['avg_positive']:.2f}", 
             f"{sentiment_summary['max_positive']:.2f}", 
             f"{sentiment_summary['min_positive']:.2f}"],
            ['Neutral', f"{sentiment_summary['avg_neutral']:.2f}", '-', '-'],
            ['Negative', f"{sentiment_summary['avg_negative']:.2f}", 
             f"{sentiment_summary['max_negative']:.2f}", 
             f"{sentiment_summary['min_negative']:.2f}"],
        ]
        
        sentiment_table = Table(sentiment_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        sentiment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4bc0c0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(sentiment_table)
        elements.append(Spacer(1, 20))
    
    # Top Sources
    elements.append(PageBreak())
    elements.append(Paragraph("Top 10 News Sources", heading_style))
    
    source_counts = Counter([a.get('source_name', 'Unknown') for a in articles])
    top_sources = source_counts.most_common(10)
    
    source_data = [['Rank', 'Source', 'Articles']]
    for idx, (source, count) in enumerate(top_sources, 1):
        source_data.append([str(idx), source, str(count)])
    
    source_table = Table(source_data, colWidths=[0.7*inch, 3.5*inch, 1*inch])
    source_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(source_table)
    elements.append(Spacer(1, 20))
    
    # Sentiment Distribution
    sentiment_counts = Counter([a.get('sentiment', 'neutral') or 'neutral' for a in articles])

    sentiment_dist_data = [['Sentiment', 'Count', 'Percentage']]
    total = len(articles)
    for sentiment, count in sentiment_counts.items():
        percentage = (count / total) * 100
        sentiment_name = str(sentiment).capitalize() if sentiment else 'Unknown'
        sentiment_dist_data.append([sentiment_name, str(count), f"{percentage:.2f}%"])
    
    sentiment_dist_table = Table(sentiment_dist_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
    sentiment_dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4bc0c0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(Paragraph("Sentiment Distribution", heading_style))
    elements.append(sentiment_dist_table)
    
    # Footer
    elements.append(Spacer(1, 30))
    footer_text = Paragraph(
        "Generated by NewsData.io Analysis Dashboard | Visit newsdata.io for more information",
        styles['Normal']
    )
    elements.append(footer_text)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


# Main content area
if not api_key:
    st.warning("⚠️ Please enter your NewsData.io API key in the sidebar to get started.")
    st.info("""
    ### Getting Started:
    1. Get your free API key from [newsdata.io](https://newsdata.io)
    2. Enter it in the sidebar
    3. Configure your search filters
    4. Click 'Search News' to begin!
    """)
else:
    # Search button
    col1, col2 = st.columns([1, 5])
    with col1:
        search_clicked = st.button("🔍 Search News", use_container_width=True)
    
    # Handle search
    if search_clicked:
        st.session_state.articles = []
        st.session_state.analysis_done = False
        
        try:
            with st.spinner("Fetching initial results..."):
                url, params = build_api_url(api_key, endpoint)
                response = requests.get(url, params=params, timeout=30)
                data = response.json()
                
                if data.get("status") == "error":
                    st.error(f"API Error: {data.get('results', {}).get('message', 'Unknown error')}")
                else:
                    st.session_state.total_results = data.get("totalResults", 0)
                    st.success(f"✅ Found **{st.session_state.total_results:,}** total results!")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Show total results and generate analysis button
    if st.session_state.total_results > 0:
        st.info(f"📊 **Total Results Found:** {st.session_state.total_results:,}")
        
        # Display API URL and Parameters
        with st.expander("🔗 View API Request Details", expanded=False):
            st.code(f"Endpoint: {st.session_state.api_url}", language="text")
            st.write("**Parameters:**")
            for key, value in st.session_state.api_params.items():
                st.write(f"• **{key}:** {value}")
        
        if st.button("📊 Generate Analysis", use_container_width=False):
            st.session_state.analysis_done = False
            
            # Progress tracking
            st.markdown("### 🔄 Fetching Articles...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Fetch all articles
            articles = fetch_all_news(api_key, endpoint, progress_bar, status_text)
            st.session_state.articles = articles
            st.session_state.analysis_done = True
            
            st.success(f"✅ Analysis complete! Fetched **{len(articles):,}** articles.")
    
    # Display analysis
    if st.session_state.analysis_done and st.session_state.articles:
        articles = st.session_state.articles
        
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")
        
        # Statistics
        generate_stats(articles)
        
        st.markdown("---")
        
        # Sentiment Analysis Results
        st.markdown("### 😊 Detailed Sentiment Analysis")
        sentiment_summary = get_sentiment_summary(articles)
        
        if sentiment_summary:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Average Positive Sentiment",
                    f"{sentiment_summary['avg_positive']:.2f}%",
                    f"Max: {sentiment_summary['max_positive']:.2f}%"
                )
            
            with col2:
                st.metric(
                    "Average Neutral Sentiment",
                    f"{sentiment_summary['avg_neutral']:.2f}%"
                )
            
            with col3:
                st.metric(
                    "Average Negative Sentiment",
                    f"{sentiment_summary['avg_negative']:.2f}%",
                    f"Max: {sentiment_summary['max_negative']:.2f}%"
                )
            
            # Sentiment Details Table
            st.markdown("#### Sentiment Score Details")
            sentiment_df = pd.DataFrame({
                'Sentiment Type': ['Positive', 'Neutral', 'Negative'],
                'Average (%)': [
                    f"{sentiment_summary['avg_positive']:.2f}",
                    f"{sentiment_summary['avg_neutral']:.2f}",
                    f"{sentiment_summary['avg_negative']:.2f}"
                ],
                'Maximum (%)': [
                    f"{sentiment_summary['max_positive']:.2f}",
                    "-",
                    f"{sentiment_summary['max_negative']:.2f}"
                ],
                'Minimum (%)': [
                    f"{sentiment_summary['min_positive']:.2f}",
                    "-",
                    f"{sentiment_summary['min_negative']:.2f}"
                ]
            })
            st.dataframe(sentiment_df, use_container_width=True)
        
        st.markdown("---")
        
        # Word Cloud
        st.markdown("### ☁️ Keywords Word Cloud")
        wordcloud = generate_wordcloud(articles)
        
        if wordcloud:
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.info("No valid keywords found for word cloud generation.")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(plot_source_chart(articles), use_container_width=True)
            st.plotly_chart(plot_category_chart(articles), use_container_width=True)
            st.plotly_chart(plot_sentiment_scores(articles), use_container_width=True)
        
        with col2:
            st.plotly_chart(plot_sentiment_chart(articles), use_container_width=True)
            st.plotly_chart(plot_country_chart(articles), use_container_width=True)
            
            timeline_fig = plot_timeline(articles)
            if timeline_fig:
                st.plotly_chart(timeline_fig, use_container_width=True)
        
        # Download data
        st.markdown("---")
        st.markdown("### 💾 Download Data")
        
        # Convert to DataFrame
        df = pd.DataFrame(articles)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"newsdata_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            json_str = df.to_json(orient='records', indent=2)
            st.download_button(
                label="📥 Download as JSON",
                data=json_str,
                file_name=f"newsdata_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col3:
            # PDF Export
            pdf_buffer = export_to_pdf(articles, sentiment_summary)
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name=f"newsdata_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        
        # Show sample articles
        st.markdown("---")
        st.markdown("### 📰 Sample Articles")
        
        if st.checkbox("Show sample articles (first 10)"):
            for i, article in enumerate(articles[:10], 1):
                with st.expander(f"{i}. {article.get('title', 'No Title')}"):
                    st.write(f"**Source:** {article.get('source_name', 'Unknown')}")
                    st.write(f"**Published:** {article.get('pubDate', 'Unknown')}")
                    st.write(f"**Sentiment:** {article.get('sentiment', 'Unknown')}")
                    if article.get('description'):
                        st.write(f"**Description:** {article['description']}")
                    if article.get('link'):
                        st.write(f"**[Read Full Article]({article['link']})**")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>📊 NewsData.io Analysis Dashboard | Made with ❤️ using Streamlit</p>
    <p>Visit <a href='https://newsdata.io' target='_blank'>NewsData.io</a> for API documentation</p>
</div>
""", unsafe_allow_html=True)
