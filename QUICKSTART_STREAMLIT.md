# Quick Start Guide - Streamlit Version

## 🚀 Get Running in 2 Minutes

### Installation
```bash
# 1. Install dependencies (30 seconds)
pip install -r requirements.txt

# 2. Run the app (10 seconds)
streamlit run app.py
```

**That's it!** The app opens automatically in your browser.

---

## 📚 Example Workflows

### Example 1: Latest Tech News Analysis
```
1. Enter API key in sidebar
2. Select "Latest News"
3. Set filters:
   - Search Query: "artificial intelligence"
   - Category: technology
   - Time Range: 24 hours
4. Click "Search News"
5. Click "Generate Analysis"
6. Wait ~30 seconds
7. Explore charts and download data!
```

**Expected Results**: 500-1000 articles, sentiment breakdown, top tech sources

---

### Example 2: Crypto Market Sentiment
```
1. Select "Crypto News"
2. Enter coins: btc,eth,sol
3. Time Range: 48 hours
4. Search → Generate Analysis
5. Check sentiment distribution
6. Export as CSV for reports
```

**Use Case**: Daily crypto sentiment tracking for trading decisions

---

### Example 3: Historical Election Coverage
```
1. Select "Archive News"
2. Search: "election"
3. Category: Politics
4. Date Range: Last 30 days
5. Generate Analysis
6. Review timeline chart for trends
```

**Insight**: See how coverage and sentiment evolved over time

---

## 🎯 Common Tasks

### Task: Export Data for Excel
```
1. Run your analysis
2. Scroll to "Download Data" section
3. Click "Download as CSV"
4. Open in Excel/Google Sheets
```

### Task: Compare Multiple Searches
```
1. Run first search → Download CSV
2. Reset filters (sidebar button)
3. Run second search → Download CSV
4. Compare in Excel/Python/R
```

### Task: Monitor Breaking News
```
1. Select "Latest News"
2. Time Range: 1-2 hours
3. Set relevant keywords
4. Generate Analysis
5. Refresh page to re-run
```

---

## 💡 Pro Tips

### Tip 1: Use Session State
The app remembers your last analysis. You can:
- Scroll through charts
- Download data multiple times
- Adjust view without re-fetching

### Tip 2: Filter First, Then Analyze
```
✅ Good: Specific filters → 500 articles → Fast
❌ Bad: No filters → 10,000 articles → Slow
```

### Tip 3: Sidebar Stays Open
All controls in sidebar = easy access while viewing charts

### Tip 4: Check Sample Articles
Enable "Show sample articles" to verify data quality

### Tip 5: Download Both Formats
- CSV for Excel/Sheets
- JSON for Python/JavaScript processing

---

## 🔧 Troubleshooting

### Problem: App won't start
```bash
# Solution 1: Update pip
pip install --upgrade pip

# Solution 2: Install individually
pip install streamlit requests pandas plotly wordcloud matplotlib

# Solution 3: Use Python 3.9+
python --version
```

### Problem: "Rate limit reached"
```
✅ Solution: Wait 5 minutes, then try again
✅ Partial results are already shown
✅ Consider smaller date ranges
```

### Problem: Charts not showing
```bash
# Clear Streamlit cache
streamlit cache clear

# Update libraries
pip install --upgrade plotly streamlit
```

### Problem: Word cloud is blank
```
✅ This means no valid keywords in data
✅ Try different search terms
✅ Some sources don't provide keywords
```

---

## 📊 Understanding Your Analysis

### Statistics Cards
- **Articles Analyzed**: How many articles were fetched
- **Unique Sources**: Number of different news outlets
- **Avg Positive Sentiment**: Overall positivity (30-40% is typical)
- **Countries Covered**: Geographic diversity

### Chart Meanings

**News by Source**
- Shows which outlets cover your topic most
- Horizontal bars = easy comparison
- Top 10 sources only

**Sentiment Distribution**
- Pie chart of positive/neutral/negative
- High negative = crisis/controversy
- High positive = good news/hype

**Category Distribution**
- How articles are classified
- Donut chart for clarity
- Shows topic overlap

**Timeline Chart**
- Line graph showing publication dates
- Spikes = breaking stories
- Trends = sustained coverage

**Word Cloud**
- Bigger words = more frequent keywords
- Filters out noise (null, single occurrences)
- Quick topic overview

---

## 🎨 Customization Quick Tips

### Change Colors
In `app.py`, find and edit:
```python
color_discrete_sequence=['#667eea']  # Your color here
```

### Adjust Chart Size
```python
fig.update_layout(height=400)  # Change 400 to your preference
```

### Modify Page Limit
```python
max_pages = 50  # Line ~160 in app.py
```

---

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (FREE)
```
1. Push to GitHub
2. Visit share.streamlit.io
3. Connect repo
4. Deploy!
```
**Best for**: Sharing with team, public dashboards

### Option 2: Local Network
```bash
streamlit run app.py --server.address 0.0.0.0
```
Access from other devices: `http://YOUR_IP:8501`

### Option 3: Heroku (Free tier available)
```bash
# Create Procfile
echo "web: streamlit run app.py" > Procfile

# Deploy
heroku create
git push heroku main
```

---

## 📱 Mobile Usage

The Streamlit app is responsive:
- ✅ Sidebar collapses on mobile
- ✅ Charts adapt to screen size
- ✅ Touch-friendly controls
- ✅ Pinch-to-zoom on charts

---

## 🔐 Security Best Practices

### For Local Use
```python
# No special setup needed
# API key in sidebar only
```

### For Shared Deployment
```toml
# Create .streamlit/secrets.toml
NEWSDATA_API_KEY = "your_key"
```

```python
# In app.py, use:
api_key = st.secrets.get("NEWSDATA_API_KEY", "")
```

### For Production
- Use environment variables
- Enable HTTPS
- Add authentication (Streamlit Auth)
- Rate limit requests

---

## 🎓 Advanced Usage

### Schedule Automatic Reports
```python
# Use cron job or Task Scheduler
# Run: python automated_report.py

import subprocess
import datetime

def run_analysis():
    result = subprocess.run(['streamlit', 'run', 'app.py'])
    # Save results
    
if __name__ == "__main__":
    run_analysis()
```

### Integrate with Database
```python
# Add to app.py
import sqlite3

def save_to_db(articles):
    conn = sqlite3.connect('news.db')
    df = pd.DataFrame(articles)
    df.to_sql('articles', conn, if_exists='append')
    conn.close()
```

### API Response Caching
```python
# Add caching decorator
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_all_news(api_key, endpoint_type):
    # Your existing code
    pass
```

---

## 📈 Performance Tips

### For Large Datasets
```python
# Limit article count
if len(articles) > 5000:
    articles = articles[:5000]
```

### For Faster Loading
```python
# Cache static data
@st.cache_resource
def load_categories():
    return ["business", "tech", ...]
```

### For Better UX
```python
# Add loading messages
with st.spinner("Analyzing sentiment..."):
    # Your code
```

---

## 🆘 Getting Help

### Streamlit Documentation
```bash
streamlit docs
# Opens documentation in browser
```

### Check Versions
```bash
streamlit --version
python --version
pip list | grep streamlit
```

### Community Support
- [Streamlit Forum](https://discuss.streamlit.io/)
- [NewsData.io Support](https://newsdata.io/contact)
- Stack Overflow: Tag `streamlit`

---

## ✅ Checklist for First Run

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] NewsData.io API key ready
- [ ] Run `streamlit run app.py`
- [ ] Enter API key in sidebar
- [ ] Try a simple search
- [ ] Generate analysis
- [ ] Download data
- [ ] Explore charts

---

## 🎉 You're Ready!

Key Commands:
```bash
# Run the app
streamlit run app.py

# Stop the app
Ctrl+C (or Cmd+C on Mac)

# Clear cache
streamlit cache clear

# Update Streamlit
pip install --upgrade streamlit
```

**Start analyzing news now!** 📊

---

**Happy Analyzing with Streamlit! 🚀**
