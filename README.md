# NewsData.io Analysis Dashboard

A comprehensive Python-based dashboard built with Streamlit for analyzing news data from NewsData.io with advanced visualizations, sentiment analysis, PDF export, and detailed reporting.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28.2-red)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Table of Contents

- [Features](#-features)
- [New Features](#-new-features-latest-update)
- [Installation](#-installation)
- [Usage](#-usage)
- [Exports](#-exports)
- [Troubleshooting](#-troubleshooting)
- [Future Scope](#-future-scope)

---

## 🌟 Features

### Core Functionality
✅ **3 API Endpoints Support**
- Latest News (past 48 hours)
- Crypto News (cryptocurrency-specific)
- Archive News (up to 7 years historical data)

✅ **Advanced Filtering**
- Search by keywords
- Geographic filters (country, language)
- Content filters (category, sentiment, domain)
- Crypto coin filtering
- Time range selection

✅ **Interactive Visualizations**
- 6 Plotly interactive charts
- Keyword word cloud
- Real-time progress tracking
- Responsive design

✅ **Data Analysis**
- Statistics dashboard
- Sentiment distribution analysis
- Source credibility metrics
- Geographic coverage analysis
- Timeline trends

✅ **Export Capabilities**
- CSV export
- JSON export
- PDF Report (NEW!)

---

## 🆕 New Features (Latest Update)

### 1. PDF Export with Comprehensive Report 📄
Professional PDF reports including:
- Summary statistics
- **Detailed sentiment analysis** (avg, max, min scores)
- Top 10 news sources
- Sentiment distribution
- API request details
- Timestamp and metadata

### 2. API URL Display 🔗
View the actual API request:
- Complete endpoint URL
- All parameters used
- Expandable section
- Useful for debugging

### 3. Enhanced Sentiment Analysis 😊
Detailed sentiment metrics:
- Average positive/neutral/negative percentages
- Maximum sentiment scores
- Minimum sentiment scores
- Interactive metric cards
- Detailed data table

---

## 🚀 Installation

### Windows

#### Quick Setup
1. Extract ZIP file
2. Double-click `setup.bat`
3. Double-click `run.bat`

#### Manual Setup
```cmd
cd newsdata-streamlit-dashboard
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

---

### Linux

#### Quick Setup
```bash
cd newsdata-streamlit-dashboard
chmod +x setup.sh run.sh
./setup.sh
./run.sh
```

#### Manual Setup
```bash
cd newsdata-streamlit-dashboard
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

---

## 📖 Usage

### Step 1: Get API Key
1. Visit [NewsData.io](https://newsdata.io)
2. Sign up for free
3. Copy API key

### Step 2: Launch Dashboard
```bash
# Windows
run.bat

# Linux
./run.sh
```

### Step 3: Configure Search
1. Enter API key in sidebar
2. Select endpoint
3. Set filters
4. Click "Search News"
5. Click "Generate Analysis"

### Step 4: Explore Results
- View statistics and charts
- Check detailed sentiment analysis
- View API request details
- Download reports (CSV/JSON/PDF)

---

## 📊 Exports

### CSV Export
- Excel-compatible
- All article data
- Metadata included

### JSON Export
- Developer-friendly
- Complete data structure
- Easy to parse

### PDF Report (NEW!)
Professional report with:
- Summary statistics
- API request details
- **Detailed sentiment analysis** (average, max, min scores)
- Top 10 sources
- Sentiment distribution
- Timestamp

---

## 🔧 Troubleshooting

### Installation

**"Python not found"**
```bash
# Windows: Download from python.org
# Linux: sudo apt install python3 python3-pip python3-venv
```

**Package installation fails**
```bash
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

**Permission denied (Linux)**
```bash
chmod +x setup.sh run.sh
```

### Runtime

**"Rate limit reached"**
- Wait 5 minutes
- Use smaller date ranges
- Partial results shown

**Port already in use**
```bash
streamlit run app.py --server.port 8502
```

**Charts not displaying**
```bash
streamlit cache clear
pip install --upgrade plotly
```

**PDF export fails**
```bash
pip install reportlab==4.0.7 kaleido==0.2.1
```

---

## 🔮 Future Scope

### Planned Features

#### Phase 1: Enhanced Analytics
- Multi-search comparison
- Trend detection
- Source credibility scoring
- Custom date grouping
- Advanced filtering UI

#### Phase 2: Automation
- Email report scheduling
- Database integration
- API response caching
- Custom alert triggers
- Webhook integration

#### Phase 3: Advanced Features
- Natural Language Queries
- AI-powered summarization
- Topic modeling
- Network analysis
- Real-time monitoring

#### Phase 4: Enterprise
- Multi-user support
- Role-based access
- Custom branding
- Advanced security
- API rate limiting

#### Phase 5: Data Enhancements
- Image analysis
- Video content processing
- Social media integration
- Cross-reference checking
- Language translation

### Technical Improvements
- Performance optimization
- Docker deployment
- Kubernetes support
- GraphQL API
- WebSocket updates

### UI/UX
- Dark mode
- Custom dashboards
- Mobile app
- Accessibility improvements
- Internationalization

---

## 📄 Dependencies

```txt
streamlit==1.28.2      # Web framework
requests==2.31.0       # HTTP requests
pandas==2.0.3          # Data manipulation
plotly==5.18.0         # Interactive charts
wordcloud==1.9.3       # Word cloud generation
matplotlib==3.7.5      # Chart rendering
reportlab==4.0.7       # PDF generation
kaleido==0.2.1         # Chart export
```

---

## 🎯 Quick Commands

```bash
# Install
pip install -r requirements.txt

# Run
streamlit run app.py

# Stop
Ctrl + C

# Deactivate venv
deactivate
```

---

## 📞 Support

- [Streamlit Docs](https://docs.streamlit.io)
- [NewsData.io API](https://newsdata.io/documentation)
- [GitHub Issues](https://github.com/yourusername/newsdata-dashboard/issues)

---

## 🙏 Acknowledgments

- [NewsData.io](https://newsdata.io) for excellent API
- [Streamlit](https://streamlit.io) for amazing framework
- [Plotly](https://plotly.com) for interactive charts
- Open-source community

---

**Made with ❤️ using Python & Streamlit**

**Happy Analyzing! 📊**
