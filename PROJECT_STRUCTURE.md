# Project Structure

## 📁 File Organization

```
newsdata-streamlit-dashboard/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README_STREAMLIT.md            # Full documentation
├── QUICKSTART_STREAMLIT.md        # Quick start guide
├── PROJECT_STRUCTURE.md           # This file
├── setup.bat                      # Windows setup script
├── setup.sh                       # Linux/Mac setup script
├── run.bat                        # Windows run script
├── run.sh                         # Linux/Mac run script
└── .streamlit/
    └── config.toml                # Streamlit configuration
```

## 📄 File Descriptions

### Core Files

#### `app.py`
- Main application file
- Contains all dashboard logic
- ~500 lines of Python code
- Single-file architecture for easy deployment

**Key Components:**
- Streamlit UI configuration
- API integration with NewsData.io
- Data fetching with pagination
- Chart generation (Plotly)
- Word cloud generation
- Export functionality (CSV/JSON)

**Functions:**
- `build_api_url()` - Constructs API URLs with filters
- `clean_keywords()` - Removes null values from keywords
- `fetch_all_news()` - Fetches articles with pagination
- `generate_stats()` - Creates statistics cards
- `plot_source_chart()` - Source distribution chart
- `plot_sentiment_chart()` - Sentiment pie chart
- `plot_category_chart()` - Category distribution
- `plot_country_chart()` - Country coverage
- `plot_sentiment_scores()` - Average sentiment scores
- `plot_timeline()` - Timeline chart
- `generate_wordcloud()` - Keyword visualization

#### `requirements.txt`
Python package dependencies:
```
streamlit==1.31.0      # Web framework
requests==2.31.0       # HTTP requests
pandas==2.2.0          # Data manipulation
plotly==5.18.0         # Interactive charts
wordcloud==1.9.3       # Word cloud generation
matplotlib==3.8.2      # Chart rendering
```

### Documentation Files

#### `README_STREAMLIT.md`
Complete documentation including:
- Features overview
- Installation instructions
- Usage guide
- Customization options
- Deployment guides
- Troubleshooting
- API reference

#### `QUICKSTART_STREAMLIT.md`
Quick reference guide:
- 2-minute setup
- Example workflows
- Common tasks
- Pro tips
- Troubleshooting quick fixes

### Configuration Files

#### `.streamlit/config.toml`
Streamlit app configuration:
- Theme colors (purple/blue gradient)
- Server settings
- Browser settings
- Performance options

**Customizable Options:**
```toml
[theme]
primaryColor = "#667eea"           # Main accent color
backgroundColor = "#ffffff"        # Page background
secondaryBackgroundColor = "#f0f2f6"  # Sidebar background
textColor = "#262730"              # Text color

[server]
port = 8501                        # Server port
headless = true                    # Run without browser prompt
```

### Setup Scripts

#### `setup.bat` (Windows)
Automated setup for Windows:
1. Checks Python installation
2. Installs dependencies
3. Provides next steps

#### `setup.sh` (Linux/Mac)
Automated setup for Unix systems:
1. Checks Python 3 installation
2. Installs dependencies via pip3
3. Provides next steps

### Run Scripts

#### `run.bat` (Windows)
Quick launcher for Windows:
- Starts Streamlit server
- Opens browser automatically

#### `run.sh` (Linux/Mac)
Quick launcher for Unix:
- Starts Streamlit server
- Opens browser automatically

## 🔧 How It Works

### Application Flow

```
1. User opens app → Streamlit loads
2. User enters API key → Stored in session state
3. User selects endpoint → Updates filter options
4. User configures filters → Builds API URL
5. User clicks "Search" → Fetches total results
6. User clicks "Generate Analysis" → Fetches all pages
7. Progress bar updates → Real-time feedback
8. Data processed → Charts generated
9. Results displayed → Interactive Plotly charts
10. User downloads data → CSV/JSON export
```

### Data Flow

```
NewsData.io API
      ↓
  requests.get()
      ↓
  JSON Response
      ↓
  Python Dict
      ↓
  Pandas DataFrame
      ↓
  Plotly Charts
      ↓
  Streamlit Display
```

### Session State Management

```python
st.session_state.articles = []         # Fetched articles
st.session_state.total_results = 0     # Total count
st.session_state.analysis_done = False # Analysis status
```

## 🎨 Customization Points

### 1. Colors and Theme
**File:** `.streamlit/config.toml`
```toml
primaryColor = "#667eea"  # Change to your brand color
```

**File:** `app.py` (CSS section)
```python
st.markdown("""
    <style>
    .stProgress > div > div > div > div {
        background-color: #667eea;  # Progress bar color
    }
    </style>
""", unsafe_allow_html=True)
```

### 2. Chart Settings
**File:** `app.py`

Chart colors:
```python
color_discrete_sequence=['#667eea']  # Single color charts
color_discrete_map={'Positive': '#4bc0c0', ...}  # Multi-color
```

Chart heights:
```python
fig.update_layout(height=400)  # Adjust as needed
```

### 3. API Settings
**File:** `app.py`

Pagination limits:
```python
max_pages = 50  # Maximum pages to fetch
```

Archive delay:
```python
time.sleep(1)  # Delay between requests
```

Request timeout:
```python
response = requests.get(url, params=params, timeout=30)
```

### 4. Filter Options
**File:** `app.py`

Add more languages:
```python
language = st.selectbox("Language", 
    ["", "en", "es", "fr", "de", "it", "pt", "ar", "zh", "ja", "hi", "ko", "ru"]
)
```

Add more categories:
```python
category = st.sidebar.selectbox("Category",
    ["", "business", "tech", "sports", "custom_category"]
)
```

## 📊 Chart Specifications

### Source Chart
- Type: Horizontal Bar
- Library: Plotly Express
- Top: 10 sources
- Color: Purple (#667eea)

### Sentiment Chart
- Type: Pie
- Library: Plotly Express
- Colors: Teal (positive), Yellow (neutral), Red (negative)

### Category Chart
- Type: Donut (Pie with hole)
- Library: Plotly Express
- Top: 8 categories
- Hole size: 0.3

### Country Chart
- Type: Horizontal Bar
- Library: Plotly Express
- Top: 10 countries
- Color: Purple (#9966ff)

### Sentiment Scores
- Type: Bar
- Library: Plotly Express
- Shows: Average percentages
- Colors: Match sentiment chart

### Timeline Chart
- Type: Line with fill
- Library: Plotly Express
- Fill: Gradient under line
- Markers: True

### Word Cloud
- Library: WordCloud + Matplotlib
- Size: 800x400
- Colormap: Viridis
- Min frequency: 2 occurrences

## 🔐 Security Considerations

### API Key Storage
- Stored in session state (memory only)
- Not persisted to disk
- Cleared on page refresh

### For Production
1. Use Streamlit secrets:
```toml
# .streamlit/secrets.toml
NEWSDATA_API_KEY = "your_key"
```

2. Add authentication:
```python
import streamlit_authenticator as stauth
```

3. Enable HTTPS
4. Rate limit requests
5. Validate inputs

## 🚀 Deployment Options

### 1. Streamlit Cloud (Recommended)
- Free tier available
- Automatic HTTPS
- GitHub integration
- Custom domain support

### 2. Heroku
```
Procfile: web: streamlit run app.py --server.port=$PORT
```

### 3. Docker
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### 4. AWS EC2/Azure/GCP
- Install Python 3.8+
- Clone repository
- Run setup script
- Configure reverse proxy (nginx)

## 📈 Performance Optimization

### Caching
```python
@st.cache_data(ttl=3600)
def fetch_all_news(...):
    # Cached for 1 hour
```

### Lazy Loading
```python
# Only load charts when data is ready
if st.session_state.analysis_done:
    # Generate charts
```

### Memory Management
```python
# Limit article storage
if len(articles) > 10000:
    articles = articles[:10000]
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] All endpoints work (Latest, Crypto, Archive)
- [ ] All filters apply correctly
- [ ] Progress bar updates
- [ ] Charts render properly
- [ ] Downloads work (CSV/JSON)
- [ ] Error handling works
- [ ] Rate limit detection works

### Test Data
Use these filters for quick testing:
```
Endpoint: Latest News
Search: "technology"
Category: technology
Language: en
Time Range: 24 hours
```

## 📝 Development Notes

### Adding New Features

1. **New Chart Type:**
   - Add function: `def plot_new_chart(articles):`
   - Add to display section
   - Use Plotly for consistency

2. **New Filter:**
   - Add to sidebar section
   - Update `build_api_url()` function
   - Test with API

3. **New Export Format:**
   - Add conversion logic
   - Add download button
   - Update documentation

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings
- Comment complex logic

## 🐛 Known Issues

1. **Word Cloud**: May fail if no valid keywords
   - Solution: Shows info message

2. **Timeline Chart**: Empty if no dates
   - Solution: Returns None, not displayed

3. **Rate Limits**: Can't fetch all articles
   - Solution: Shows partial results

## 📞 Support Resources

- Streamlit Docs: https://docs.streamlit.io
- NewsData.io API: https://newsdata.io/documentation
- Plotly Docs: https://plotly.com/python/
- Community: https://discuss.streamlit.io/

---

**Last Updated:** February 2026
**Version:** 1.0.0
**Maintainer:** Your Team
