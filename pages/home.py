# pages/home.py
import streamlit as st

def app():
    """Interactive home page showcasing all dashboard features"""
    
    # Custom CSS for beautiful styling
    st.markdown("""
        <style>
        /* Title background container */
        .title-container {
            background: linear-gradient(135deg, #ff6b35 0%, #f7931e 50%, #ff9a56 100%);
            padding: 3rem 2rem;
            border-radius: 25px;
            margin-bottom: 2rem;
            box-shadow: 0 15px 50px rgba(255, 107, 53, 0.4);
            position: relative;
            overflow: hidden;
            border: 3px solid rgba(255, 255, 255, 0.3);
            animation: fadeInDown 1s ease-in;
        }
        
        /* Animated background pattern */
        .title-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 10px,
                rgba(255, 255, 255, 0.05) 10px,
                rgba(255, 255, 255, 0.05) 20px
            );
            animation: slide 20s linear infinite;
        }
        
        @keyframes slide {
            0% { transform: translate(0, 0); }
            100% { transform: translate(50px, 50px); }
        }
        
        /* Title styling */
        .main-title {
            text-align: center;
            font-size: 3.5rem;
            font-weight: 800;
            color: white;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
            position: relative;
            z-index: 1;
        }
        
        .subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: rgba(255, 255, 255, 0.95);
            margin-bottom: 0;
            position: relative;
            z-index: 1;
            text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.2);
        }
        
        /* Card container */
        .card-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }
        
        /* Individual cards */
        .feature-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 2.5rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.8s ease-in;
        }
        
        .feature-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.5);
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .feature-card:hover::before {
            left: 100%;
        }
        
        .card-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: bounce 2s infinite;
        }
        
        .card-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
            margin-bottom: 0.8rem;
        }
        
        .card-description {
            font-size: 1rem;
            color: rgba(255, 255, 255, 0.9);
            line-height: 1.6;
        }
        
        /* Different gradient for each card */
        .card-1 { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        .card-2 { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
        .card-3 { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
        .card-4 { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
        
        /* Animations */
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
        
        /* Stats section */
        .stats-container {
            display: flex;
            justify-content: space-around;
            margin: 3rem 0;
            padding: 2rem;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            animation: fadeIn 2s ease-in;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 800;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 1rem;
            color: #666;
            margin-top: 0.5rem;
        }
        
        /* Welcome section */
        .welcome-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            text-align: center;
            animation: fadeIn 1s ease-in;
        }
        
        .welcome-box h3 {
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Main title with stylish background
    st.markdown("""
        <div class="title-container">
            <h1 class="main-title">🏏 Cricbuzz Live Statistical Dashboard</h1>
            <p class="subtitle">Your Ultimate Cricket Analytics Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
        <div class="welcome-box">
            <h3>Welcome to Cricket Data World!</h3>
            <p>Explore real-time scores, player statistics, advanced analytics, and manage your cricket data all in one place.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats overview
    st.markdown("""
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">4</div>
                <div class="stat-label">Powerful Features</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">∞</div>
                <div class="stat-label">Live Updates</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Data Access</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 🎯 Explore Our Features")
    
    # Create 4 interactive cards for each page
    col1, col2 = st.columns(2)
    
    with col1:
        # Card 1: Live Scores
        st.markdown("""
            <div class="feature-card card-1">
                <div class="card-icon">🔴</div>
                <div class="card-title">Live Scores</div>
                <div class="card-description">
                    Watch cricket matches unfold in real-time! Get live scores, ball-by-ball updates, 
                    and upcoming match schedules from the Cricbuzz API.
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("")
        if st.button("🏏 View Live Scores", key="btn_live", use_container_width=True):
            st.info("🔄 Please select '🏏 Live Scores' from the sidebar to view live matches!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Card 3: SQL Analytics
        st.markdown("""
            <div class="feature-card card-3">
                <div class="card-icon">📊</div>
                <div class="card-title">SQL Analytics</div>
                <div class="card-description">
                    Run advanced SQL queries on cricket data! Analyze player performance, 
                    match statistics, and uncover insights with powerful analytics.
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("")
        if st.button("📈 Run Analytics", key="btn_sql", use_container_width=True):
            st.info("🔄 Please select '📊 SQL Analytics' from the sidebar to run queries!")
    
    with col2:
        # Card 2: Player Stats
        st.markdown("""
            <div class="feature-card card-2">
                <div class="card-icon">👤</div>
                <div class="card-title">Player Statistics</div>
                <div class="card-description">
                    Discover detailed player profiles and statistics! Search for your favorite 
                    cricketers and explore their career achievements and rankings.
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("")
        if st.button("🔍 Search Players", key="btn_players", use_container_width=True):
            st.info("🔄 Please select '👤 Player Stats' from the sidebar to search players!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Card 4: CRUD Operations
        st.markdown("""
            <div class="feature-card card-4">
                <div class="card-icon">🛠️</div>
                <div class="card-title">CRUD Operations</div>
                <div class="card-description">
                    Manage your cricket database! Add, update, delete, and view match data, 
                    player records, and venue information with ease.
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("")
        if st.button("⚙️ Manage Data", key="btn_crud", use_container_width=True):
            st.info("🔄 Please select '🛠️ CRUD Operations' from the sidebar to manage data!")
    
    # Footer section
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 15px; margin-top: 2rem;">
            <h3 style="color: #667eea; margin-bottom: 1rem;">🚀 Getting Started</h3>
            <p style="color: #666; font-size: 1.1rem;">
                Select any feature from the <strong>sidebar menu</strong> to begin your cricket analytics journey!
            </p>
            <p style="color: #999; font-size: 0.9rem; margin-top: 1rem;">
                💡 <em>Use the dropdown menu in the sidebar to navigate between different features</em>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Additional info with expanders
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("ℹ️ About This Dashboard"):
        st.markdown("""
            ### About Cricbuzz Live Statistical Dashboard
            
            This comprehensive cricket analytics platform provides:
            
            - **Real-time Data**: Live scores and upcoming matches from Cricbuzz API
            - **Player Insights**: Detailed player statistics, rankings, and profiles
            - **Advanced Analytics**: SQL-based queries for in-depth cricket analysis
            - **Data Management**: Full CRUD capabilities for match and player data
            
            Built with ❤️ using Streamlit and powered by Cricbuzz API.
        """)
    
    with st.expander("🎓 Quick Tips"):
        st.markdown("""
            ### How to Use This Dashboard
            
            1. **Navigate**: Use the sidebar dropdown to switch between features
            2. **Live Scores**: Check real-time match updates and upcoming fixtures
            3. **Player Stats**: Search for players by name to view their profiles
            4. **SQL Analytics**: Run predefined queries or create custom ones
            5. **CRUD Operations**: Manage your local cricket database
            
            💡 **Pro Tip**: Use the filters and search functions to quickly find what you need!
        """)

if __name__ == "__main__":
    app()
