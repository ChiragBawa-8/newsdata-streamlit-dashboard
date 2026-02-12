# NewsData.io Analysis Dashboard (Streamlit)

A powerful Python-based dashboard built with Streamlit for analyzing news data from NewsData.io with advanced visualizations, sentiment analysis, and real-time progress tracking.

## 🌟 Features

### 📊 Multiple Endpoints Support
- **Latest News**: Get breaking news from the past 48 hours
- **Crypto News**: Cryptocurrency-specific news filtering
- **Archive News**: Access historical news up to 7 years back

### 🔍 Advanced Filtering
- **Search Options**: Query search (q), Title search (qInTitle)
- **Geographic Filters**: Country, Language
- **Content Filters**: Category, Sentiment, Domain
- **Crypto Specific**: Filter by coin symbols (BTC, ETH, etc.)
- **Time Ranges**: 
  - Latest/Crypto: Hours (1-48) or Minutes (1-2880)
  - Archive: Date range selector (up to 7 years)

### 📈 Visual Analytics

#### Statistics Cards
- Total articles analyzed
- Unique news sources
- Average positive sentiment
- Countries covered

#### Interactive Charts (Plotly)
1. **News by Source** - Top 10 sources horizontal bar chart
2. **Sentiment Distribution** - Positive/Neutral/Negative pie chart
3. **Category Distribution** - Article categories donut chart
4. **Country Distribution** - Geographic coverage horizontal bar
5. **Sentiment Scores** - Average sentiment percentages bar chart
6. **Timeline Chart** - Articles published over time line chart

#### Word Cloud
- Visual representation of most frequent keywords
- Handles null values automatically
- Dynamic scaling based on keyword frequency
- Matplotlib-based rendering

### ⚡ Smart Features

#### Progress Tracking
- Real-time Streamlit progress bar
- Page fetch counter
- Article count updates
- Completion status

#### Rate Limit Handling
- Detects API rate limit errors (429)
- Shows partial results from successfully fetched articles
- Clear error messaging without losing data

#### Null Value Handling
- Keywords: Filters out `null`, `[null]`, `["ai", null]` scenarios
- Only processes valid, non-null keywords
- Graceful handling when no keywords available

#### Archive Endpoint Optimization
- 1-second delay between page fetches to avoid rate limits
- Progress updates during fetching
- Date range validation (up to 7 years back)

#### Data Export
- Download analysis as CSV
- Download analysis as JSON
- Timestamped filenames

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download
```bash
# Download the files or clone the repository
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install streamlit==1.31.0 requests==2.31.0 pandas==2.2.0 plotly==5.18.0 wordcloud==1.9.3 matplotlib==3.8.2
```

### Step 3: Run the App
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📋 Usage Guide

### Step 1: Enter API Key
1. Get your API key from [newsdata.io](https://newsdata.io)
2. Enter it in the sidebar (🔑 API Configuration)

### Step 2: Select Endpoint
Choose from:
- Latest News
- Crypto News
- Archive News

### Step 3: Configure Filters
Set your search parameters:
- Search terms
- Geographic filters
- Category and sentiment
- Time range
- Domain filters

### Step 4: Search
1. Click "🔍 Search News"
2. View total results count
3. Click "📊 Generate Analysis"

### Step 5: Monitor Progress
- Watch the progress bar
- See pages and articles fetched in real-time
- View completion status

### Step 6: Analyze Results
Explore:
- Statistics overview
- Interactive Plotly charts
- Keyword word cloud
- Sample articles
- Download data as CSV/JSON

## 🎨 Customization

### Change Color Scheme
Edit the color sequences in `app.py`:
```python
color_discrete_sequence=['#667eea']  # Change to your color
```

### Modify Chart Heights
```python
fig.update_layout(height=400)  # Adjust height
```

### Change Progress Limits
```python
max_pages = 50  # Increase or decrease
```

### Adjust Archive Delay
```python
time.sleep(1)  # Change delay in seconds
```

## 🛠️ Technical Details

### Libraries Used
- **Streamlit**: Web framework
- **Requests**: API calls
- **Pandas**: Data manipulation
- **Plotly**: Interactive charts
- **WordCloud**: Keyword visualization
- **Matplotlib**: Chart rendering

### Rate Limiting
- Archive endpoint: 1-second delay
- Automatic rate limit detection
- Graceful error handling

### Session State
Uses Streamlit session state to persist:
- Fetched articles
- Total results count
- Analysis status

## 📱 Deployment

### Deploy to Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

### Deploy to Heroku
```bash
# Create Procfile
web: streamlit run app.py --server.port=$PORT
```

### Deploy to AWS/Azure/GCP
Use Docker or Python runtime with:
```bash
streamlit run app.py --server.port 8501
```

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Rate limit reached"
- Wait a few minutes
- Results from fetched pages are shown
- Consider upgrading API plan

### Charts not displaying
```bash
pip install --upgrade plotly
streamlit cache clear
```

### Word cloud errors
```bash
pip install --upgrade wordcloud matplotlib
```

## 📊 Sample API Response
```json
{
  "status": "success",
  "totalResults": 15605,
  "results": [
    {
      "article_id": "...",
      "title": "...",
      "keywords": ["sport", "ai"],
      "sentiment": "neutral",
      "sentiment_stats": {
        "negative": 15.22,
        "neutral": 75.84,
        "positive": 8.94
      }
    }
  ],
  "nextPage": "..."
}
```

## 🔒 Security

- API keys stored in session state only
- No persistent storage
- All processing server-side
- HTTPS recommended for production

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [NewsData.io API Docs](https://newsdata.io/documentation)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/)

## 💡 Tips

1. **Start Small**: Use filters to limit initial results
2. **Archive Searches**: Use smaller date ranges for faster results
3. **Crypto Analysis**: Filter by 2-3 coins max for focused insights
4. **Export Data**: Download CSV for further analysis in Excel
5. **Sentiment Filter**: Use to quickly find positive/negative news

## 🔄 Features Roadmap

- [ ] Multi-search comparison
- [ ] Custom date grouping
- [ ] Advanced filtering UI
- [ ] Email report scheduling
- [ ] Database integration
- [ ] API response caching
- [ ] Custom alert triggers

## 📞 Support

- **Streamlit Issues**: [Streamlit Community](https://discuss.streamlit.io/)
- **API Issues**: [NewsData.io Support](https://newsdata.io/contact)
- **Python Help**: Check `requirements.txt` versions

## ⚖️ License

This dashboard is provided as-is for use with NewsData.io API.
Requires valid NewsData.io API key and subscription.

## 🙏 Acknowledgments

- NewsData.io for the excellent API
- Streamlit for the amazing framework
- Plotly for interactive visualizations
- Open-source community

---

**Made with ❤️ using Python & Streamlit**

## Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Run on custom port
streamlit run app.py --server.port 8080

# Run in headless mode (server)
streamlit run app.py --server.headless true
```

## Environment Variables (Optional)

Create a `.streamlit/secrets.toml` file:
```toml
NEWSDATA_API_KEY = "your_api_key_here"
```

Then access in code:
```python
api_key = st.secrets.get("NEWSDATA_API_KEY", "")
```

## Docker Deployment (Advanced)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t newsdata-dashboard .
docker run -p 8501:8501 newsdata-dashboard
```

---

**Happy Analyzing! 📊**
