# pages/top_stats.py
import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import requests
import http.client
import json

# -------------------------------
# 1) Database Connection
# -------------------------------
load_dotenv()

def create_db_connection():
    """Create MySQL database connection"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "admin"),
            database=os.getenv("DB_NAME", "cricbuzz_data")
        )
        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"❌ Database connection error: {e}")
        return None

# -------------------------------
# 2) API Functions for Player Search
# -------------------------------
BASE_URL = "cricbuzz-cricket.p.rapidapi.com"
HEADERS = {
    'x-rapidapi-key': "5525478aebmsh28bd9ab00634710p1b585fjsn2b0834636487",
    'x-rapidapi-host': "cricbuzz-cricket.p.rapidapi.com"
}

def search_player_api(player_name):
    """Search for a player using Cricbuzz API"""
    try:
        conn = http.client.HTTPSConnection(BASE_URL)
        conn.request("GET", f"/stats/v1/player/search?plrN={player_name}", headers=HEADERS)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        st.error(f"API Error: {e}")
        return {}

def get_player_details(player_id):
    """Get detailed player information"""
    try:
        conn = http.client.HTTPSConnection(BASE_URL)
        conn.request("GET", f"/stats/v1/player/{player_id}", headers=HEADERS)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        st.error(f"API Error: {e}")
        return {}

# -------------------------------
# 3) Main Streamlit Page
# -------------------------------
def app():
    st.title("📊 Player Statistics")
    st.markdown("Search players, view stats from API and Database")
    
    conn = create_db_connection()
    if not conn:
        st.warning("⚠️ Could not connect to database. Please check your .env configuration.")
        return
    
    try:
        # Create tabs - added Search tab first
        tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search Player (API)", "👥 All Players", "🏏 Batsmen ", "🎯 Bowlers"])
        
        # ===== TAB 1: SEARCH PLAYER VIA API =====
        with tab1:
            st.header("🔍 Search Player (Cricbuzz API)")
            st.markdown("Search for any cricket player and view their detailed profile")
            
            # Search input
            search_name = st.text_input("Enter player name:", placeholder="e.g., Dhoni,Raina,Kohli")

            # Initialize session state containers for persistence
            if 'last_search_players' not in st.session_state:
                st.session_state['last_search_players'] = None
            if 'last_search_term' not in st.session_state:
                st.session_state['last_search_term'] = ''
            if 'last_selected_idx' not in st.session_state:
                st.session_state['last_selected_idx'] = 0

            # Perform search when button pressed
            if st.button("🔎 Search") and search_name:
                with st.spinner("Searching..."):
                    player_data = search_player_api(search_name)

                if player_data and "player" in player_data:
                    players = player_data["player"]
                    st.session_state['last_search_players'] = players
                    st.session_state['last_search_term'] = search_name
                    st.session_state['last_selected_idx'] = 0
                else:
                    st.session_state['last_search_players'] = None
                    st.warning("No results found. Try a different search term.")

            # If there are stored players from last search, show them
            players = st.session_state.get('last_search_players')
            if players:
                if len(players) == 0:
                    st.warning(f"No players found for '{st.session_state.get('last_search_term', '')}'")
                else:
                    st.success(f"✅ Found {len(players)} player(s)")

                    # Build display names
                    player_names = [f"{p.get('name', 'Unknown')} ({p.get('teamName', p.get('team', 'N/A'))})" for p in players]

                    # Selection with persistence
                    selected_idx = st.selectbox("Select a player:", list(range(len(player_names))), index=st.session_state.get('last_selected_idx', 0), format_func=lambda x: player_names[x])
                    st.session_state['last_selected_idx'] = selected_idx
                    selected_player = players[selected_idx]

                    # Get detailed info (use id if available)
                    player_id = selected_player.get("id") or selected_player.get('playerId')
                    player_details = get_player_details(player_id) if player_id else {}

                    if player_details:
                        # Display player profile
                        st.markdown("---")
                        col1, col2 = st.columns([1, 2])

                        with col1:
                            # Try to show player image from either source
                            face_id = selected_player.get('faceImageId') or player_details.get('faceImageId')
                            if face_id:
                                img_url = f"https://www.cricbuzz.com/a/img/v1/152x152/i1/c{face_id}.jpg"
                                st.image(img_url, width=150)
                            else:
                                st.info("No image available")

                        with col2:
                            # Prefer fields from player_details, fallback to selected_player
                            display_name = player_details.get('name') or selected_player.get('name', 'Unknown')
                            team = selected_player.get('teamName') or player_details.get('teams') or selected_player.get('team', 'N/A')
                            dob = selected_player.get('dob') or player_details.get('dob') or player_details.get('birthDate')

                            st.subheader(f"👤 {display_name}")
                            st.caption(f"Team: {team}")
                            if dob:
                                st.write(f"📅 Born: {dob}")

                        # Player details in expandable sections
                        with st.expander("📋 Profile Information", expanded=True):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Role:** {player_details.get('role', 'N/A')}")
                                st.write(f"**Batting Style:** {player_details.get('bat', player_details.get('battingStyle', 'N/A'))}")
                                st.write(f"**Bowling Style:** {player_details.get('bowl', player_details.get('bowlingStyle', 'N/A'))}")
                            with col2:
                                st.write(f"**Birth Place:** {player_details.get('birthPlace', player_details.get('birthPlace', 'N/A'))}")
                                st.write(f"**Teams:** {player_details.get('teams', 'N/A')}")

                        # ICC Rankings
                        if "rankings" in player_details and player_details["rankings"]:
                            with st.expander("🏆 ICC Rankings"):
                                rankings = player_details["rankings"]
                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    st.markdown("**Batting**")
                                    if "bat" in rankings:
                                        for format_type, rank in rankings["bat"].items():
                                            st.write(f"{format_type}: {rank}")
                                    else:
                                        st.write("No rankings")

                                with col2:
                                    st.markdown("**Bowling**")
                                    if "bowl" in rankings:
                                        for format_type, rank in rankings["bowl"].items():
                                            st.write(f"{format_type}: {rank}")
                                    else:
                                        st.write("No rankings")

                                with col3:
                                    st.markdown("**All-Rounder**")
                                    if "all" in rankings:
                                        for format_type, rank in rankings["all"].items():
                                            st.write(f"{format_type}: {rank}")
                                    else:
                                        st.write("No rankings")
                    else:
                        # If no detailed API info, still show basic info from search result
                        st.markdown("---")
                        st.subheader(selected_player.get('name', 'Unknown'))
                        st.write("Basic details unavailable from API.")
        
        # ===== TAB 2: ALL PLAYERS FROM DATABASE =====
        with tab2:
            st.subheader("All Players in Database")
            
            # Sidebar filters for database
            st.sidebar.markdown("### Database Filters")
            search_db = st.sidebar.text_input("Search by name (DB)", "")
            
            # Get unique countries
            country_query = "SELECT DISTINCT country FROM players WHERE country IS NOT NULL ORDER BY country"
            countries_df = pd.read_sql(country_query, conn)
            countries = ["All"] + countries_df['country'].tolist() if not countries_df.empty else ["All"]
            selected_country = st.sidebar.selectbox("Country", countries)
            
            # Get unique roles
            role_query = "SELECT DISTINCT playing_role FROM players WHERE playing_role IS NOT NULL ORDER BY playing_role"
            roles_df = pd.read_sql(role_query, conn)
            roles = ["All"] + roles_df['playing_role'].tolist() if not roles_df.empty else ["All"]
            selected_role = st.sidebar.selectbox("Playing Role", roles)
            
            # Build query
            query = """
                SELECT 
                    player_id,
                    name,
                    country,
                    playing_role,
                    batting_style,
                    bowling_style
                FROM players
                WHERE 1=1
            """
            params = []
            
            if search_db:
                query += " AND (name LIKE %s)"
                params.append(f"%{search_db}%")
            
            if selected_country != "All":
                query += " AND country = %s"
                params.append(selected_country)
            
            if selected_role != "All":
                query += " AND playing_role = %s"
                params.append(selected_role)
            
            query += " ORDER BY player_id DESC LIMIT 100"
            
            players_df = pd.read_sql(query, conn, params=params if params else None)
            
            if players_df.empty:
                st.warning("No players found. Please add player data to your database.")
            else:
                st.success(f"📊 Found {len(players_df)} players")
                
                # Display as cards
                for _, player in players_df.iterrows():
                    with st.expander(f"👤 {player['name']} - {player['country']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("### Profile")
                            st.write(f"**Name:** {player['name']}")
                            st.write(f"**Country:** {player['country']}")
                            st.write(f"**Role:** {player['playing_role'] or 'N/A'}")
                        
                        with col2:
                            st.markdown("### Playing Style")
                            st.write(f"**Batting:** {player['batting_style'] or 'N/A'}")
                            st.write(f"**Bowling:** {player['bowling_style'] or 'N/A'}")
        
        # ---------- TAB 3: TOP BATSMEN ----------
        with tab3:
            st.subheader("🏏 Top Players - Batting Focus")
            st.info("Showing all players in the database")
            
            simple_query = """
                SELECT 
                    name,
                    country,
                    playing_role,
                    batting_style
                FROM players
                WHERE batting_style IS NOT NULL
                ORDER BY player_id DESC
                LIMIT 20
            """
            simple_df = pd.read_sql(simple_query, conn)
            
            if simple_df.empty:
                st.info("No players available in database")
            else:
                st.dataframe(simple_df, use_container_width=True)
        
        # ---------- TAB 4: TOP BOWLERS ----------
        with tab4:
            st.subheader("🎯 Top Players - Bowling Focus")
            st.info("Showing all players in the database")
            
            simple_query = """
                SELECT 
                    name,
                    country,
                    playing_role,
                    bowling_style
                FROM players
                WHERE bowling_style IS NOT NULL
                ORDER BY player_id DESC
                LIMIT 20
            """
            simple_df = pd.read_sql(simple_query, conn)
            
            if simple_df.empty:
                st.info("No players available in database")
            else:
                st.dataframe(simple_df, use_container_width=True)
        
    except Error as e:
        st.error(f"❌ Database error: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()

# -------------------------------
# 3) Run
# -------------------------------
if __name__ == "__main__":
    app()

