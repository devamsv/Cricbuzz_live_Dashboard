# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

A comprehensive cricket analytics dashboard that integrates live data from the Cricbuzz API with SQL database analytics to create an interactive web application delivering real-time match updates, detailed player statistics, and advanced SQL-driven insights.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)

---

## 📋 Table of Contents
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [SQL Queries](#-sql-queries)
- [Business Use Cases](#-business-use-cases)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## ✨ Features

### 🎯 Core Modules

#### 1. **Live Match Dashboard**
- Real-time match updates from Cricbuzz API
- Detailed scorecards with batting and bowling statistics
- Live scores, match status, and venue information
- Ball-by-ball commentary support

#### 2. **Top Player Statistics**
- Player search functionality
- Batting statistics (runs, average, strike rate, centuries)
- Bowling statistics (wickets, economy, average)
- Comprehensive player profiles with career data

#### 3. **SQL Analytics Engine**
- **25 Advanced SQL Queries** covering:
  - **Beginner Level** (Q1-Q8): Basic SELECT, WHERE, GROUP BY operations
  - **Intermediate Level** (Q9-Q16): JOINs, subqueries, aggregate functions
  - **Advanced Level** (Q17-Q25): Window functions, CTEs, complex analytics
- Interactive query execution with tabular results
- Query performance insights

#### 4. **CRUD Operations Interface**
- Full Create, Read, Update, Delete operations
- Form-based UI for easy data manipulation
- Database schema exploration
- Custom SQL query execution

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Interactive web dashboard |
| **Backend** | Python 3.8+ | Core application logic |
| **Database** | MySQL 8.0+ | Data storage and analytics |
| **API** | Cricbuzz API (RapidAPI) | Live cricket data |
| **Data Processing** | Pandas | Data manipulation and analysis |
| **HTTP Client** | Requests | API communication |

---

## 📁 Project Structure

```
cricbuzz_livedata/
│
├── app.py                          # Main Streamlit application entry point
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                       # Project documentation
├                   
│
├── pages/                          # Streamlit pages
│   ├── home.py                     # Home page with project overview
│   ├── 1.live_matches.py          # Live cricket matches page
│   ├── 2.top_stats.py             # Player statistics page
│   ├── 3.sql_query.py             # SQL analytics page (25 queries)
│   └── 4.crud_operations.py       # Database CRUD interface
│
└── utils/                          # Utility modules
    └── db_connection.py            # Database connection and operations
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- RapidAPI account (for Cricbuzz API access)

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd cricbuzz_livedata
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup MySQL Database
```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE cricbuzz;

# Import schema (if provided)
mysql -u root -p cricbuzz < schema.sql
```

---

## ⚙️ Configuration

### 1. Environment Variables Setup

Copy the example environment file and configure your credentials:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### 2. Edit `.env` File

Open `.env` and fill in your credentials:

```env
# Get API key from https://rapidapi.com/cricketapi/api/cricbuzz-cricket
RAPIDAPI_KEY=your_actual_rapidapi_key_here

# MySQL Database Credentials
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=cricbuzz
```

### 3. Get Cricbuzz API Key

1. Visit [RapidAPI Cricbuzz Cricket](https://rapidapi.com/cricketapi/api/cricbuzz-cricket)
2. Sign up or log in to RapidAPI
3. Subscribe to the Cricbuzz Cricket API (free tier available)
4. Copy your API key from the dashboard
5. Paste it into the `.env` file

---

## 💻 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Navigation

Use the sidebar to navigate between pages:

1. **🏠 Home** - Project overview and documentation
2. **🏏 Live Scores** - Real-time match updates
3. **📊 Player Stats** - Search and view player statistics
4. **📈 SQL Analytics** - Execute 25 pre-built SQL queries
5. **🛠️ CRUD Operations** - Manage database records

---

## 📊 SQL Queries

### Beginner Level (Q1-Q8)
- List players by country and role
- Recent matches with venue details
- Top run scorers and wicket-takers
- Venue capacity analysis
- Team performance statistics
- Player distribution by role
- Format-wise highest scores
- Series information

### Intermediate Level (Q9-Q16)
- All-rounder performance analysis
- Match results with detailed statistics
- Cross-format player comparison
- Home vs away team performance
- Partnership analysis
- Venue-specific bowling performance
- Close match player performance
- Year-over-year batting trends

### Advanced Level (Q17-Q25)
- Toss decision impact analysis
- Most economical bowlers
- Player consistency metrics
- Multi-format performance rankings
- Comprehensive performance ranking system
- Head-to-head team predictions
- Recent form and momentum tracking
- Best batting partnerships
- Time-series performance evolution

---

## 💼 Business Use Cases

### 1. 📺 Sports Media & Broadcasting
- Real-time match updates for commentary teams
- Player performance analysis for pre-match shows
- Historical trends for match predictions

### 2. 🎮 Fantasy Cricket Platforms
- Player form analysis for team selection
- Head-to-head statistics
- Real-time score updates for leagues

### 3. 📈 Cricket Analytics Firms
- Advanced statistical modeling
- Performance trend analysis
- Data-driven insights for team management

### 4. 🎓 Educational Institutions
- Teaching database operations with real data
- SQL practice with engaging datasets
- API integration learning

### 5. 🎲 Sports Betting & Prediction
- Historical performance analysis
- Player form tracking
- Venue-specific insights

---

## 🐛 Troubleshooting

### Common Issues

#### API Connection Error
```
❌ RAPIDAPI_KEY not found in environment variables
```
**Solution**: Ensure `.env` file exists and contains valid `RAPIDAPI_KEY`

#### Database Connection Failed
```
❌ Failed to connect to MySQL database
```
**Solution**: 
- Verify MySQL is running: `mysql --version`
- Check credentials in `.env` file
- Ensure database exists: `CREATE DATABASE cricbuzz;`

#### Missing Dependencies
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution**: Install dependencies: `pip install -r requirements.txt`

#### Port Already in Use
```
Port 8501 is already in use
```
**Solution**: 
- Stop other Streamlit apps
- Or use different port: `streamlit run app.py --server.port 8502`

---

## 📝 Development Guidelines

### Code Standards
- Follow PEP 8 Python style guidelines
- Add docstrings for all functions
- Include error handling for API calls and database operations

### Security
- Never commit `.env` file to version control
- Use environment variables for sensitive data
- Validate user inputs before SQL execution

### Testing
- Test all SQL queries before deployment
- Verify API responses handle errors gracefully
- Check database operations for edge cases

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is created as an educational assignment for learning Python, SQL, Streamlit, and API integration.

---

## 👥 Authors

**Your Name** - Cricket Analytics Enthusiast

---

## 🙏 Acknowledgments

- Cricbuzz for providing cricket data via API
- RapidAPI platform for API access
- Streamlit team for the amazing framework
- MySQL community for robust database system

---

## 📞 Support

For questions or issues:
- Check the [Troubleshooting](#-troubleshooting) section
- Review project documentation
- Contact your instructor during doubt clarification sessions (Mon-Sat, 3:30-4:30 PM)

---

**⭐ If you found this project helpful, please give it a star!**
