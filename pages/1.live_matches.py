import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

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

def get_live_scores():
    """Fetch live scores from Cricbuzz API"""
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
    headers = {
        "x-rapidapi-key": "5525478aebmsh28bd9ab00634710p1b585fjsn2b0834636487",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

def get_upcoming_matches():
    """Fetch upcoming matches from Cricbuzz API"""
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/upcoming"
    headers = {
        "x-rapidapi-key": "f44f55a4bemshca62ed26acabd9bp1f2d66jsnbd3541e61978",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

# -------------------------------
# 2) Main Streamlit Page
# -------------------------------
def app():
    st.title("🏏 Cricket Matches Dashboard")
    st.markdown("📌 “Provides real-time live scores, schedules of upcoming matches, and detailed insights from recent games.”")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🔴 Live Matches", "📅 Upcoming Matches", "📚 Recent Matches"])
    
    # ===== TAB 1: LIVE MATCHES =====
    with tab1:
        st.header("⚡ Live Matches (Real-time)")
        
        with st.spinner("Fetching live scores..."):
            live_data = get_live_scores()
        
        if live_data and "typeMatches" in live_data:
            live_match_count = 0
            
            for type_match in live_data.get("typeMatches", []):
                match_type = type_match.get("matchType", "Unknown")
                
                for series in type_match.get("seriesMatches", []):
                    series_info = series.get("seriesAdWrapper", {})
                    series_name = series_info.get("seriesName", "Unknown Series")
                    
                    if "matches" in series_info:
                        for match in series_info["matches"]:
                            match_info = match.get("matchInfo", {})
                            match_score = match.get("matchScore", {})
                            
                            team1 = match_info.get("team1", {}).get("teamName", "Team 1")
                            team2 = match_info.get("team2", {}).get("teamName", "Team 2")
                            
                            live_match_count += 1
                            
                            with st.expander(f"🔴 LIVE: {team1} vs {team2}", expanded=True):
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    st.markdown(f"**{match_info.get('matchDesc', '')}** ({match_info.get('matchFormat', '')})")
                                    st.caption(f"🏆 {series_name}")
                                    
                                    venue = match_info.get("venueInfo", {})
                                    st.write(f"📍 {venue.get('ground', '')}, {venue.get('city', '')}")
                                    st.write(f"📊 {match_info.get('status', '')}")
                                
                                with col2:
                                    st.metric("State", match_info.get("state", ""))
                                
                                # Display scores
                                if "team1Score" in match_score:
                                    t1_score = match_score.get("team1Score", {}).get("inngs1", {})
                                    st.success(f"**{team1}:** {t1_score.get('runs', 0)}/{t1_score.get('wickets', 0)} ({t1_score.get('overs', 0)} ov)")
                                
                                if "team2Score" in match_score:
                                    t2_score = match_score.get("team2Score", {}).get("inngs1", {})
                                    st.success(f"**{team2}:** {t2_score.get('runs', 0)}/{t2_score.get('wickets', 0)} ({t2_score.get('overs', 0)} ov)")
            
            if live_match_count == 0:
                st.info("🏏 No live matches at the moment. Check back later!")
            else:
                st.success(f"✅ Found {live_match_count} live matches")
        else:
            st.warning("Unable to fetch live scores from API")
    
    # ===== TAB 2: UPCOMING MATCHES =====
    with tab2:
        st.header("📅 Upcoming Matches")
        
        with st.spinner("Fetching upcoming matches..."):
            upcoming_data = get_upcoming_matches()
        
        if upcoming_data and "typeMatches" in upcoming_data:
            upcoming_match_count = 0
            
            for type_match in upcoming_data.get("typeMatches", []):
                match_type = type_match.get("matchType", "Unknown")
                
                for series in type_match.get("seriesMatches", []):
                    series_info = series.get("seriesAdWrapper", {})
                    series_name = series_info.get("seriesName", "Unknown Series")
                    
                    if "matches" in series_info:
                        for match in series_info["matches"]:
                            match_info = match.get("matchInfo", {})
                            
                            team1 = match_info.get("team1", {}).get("teamName", "Team 1")
                            team2 = match_info.get("team2", {}).get("teamName", "Team 2")
                            
                            upcoming_match_count += 1
                            
                            with st.expander(f"📅 {team1} vs {team2}"):
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    st.markdown(f"**{match_info.get('matchDesc', '')}** ({match_info.get('matchFormat', '')})")
                                    st.caption(f"🏆 {series_name}")
                                    
                                    venue = match_info.get("venueInfo", {})
                                    st.write(f"📍 {venue.get('ground', '')}, {venue.get('city', '')}")
                                    
                                    # Show start date/time
                                    start_date = match_info.get("startDate")
                                    if start_date:
                                        try:
                                            dt = datetime.fromtimestamp(int(start_date) / 1000)
                                            st.write(f"🕐 {dt.strftime('%d %b %Y, %I:%M %p')}")
                                        except:
                                            pass
                                
                                with col2:
                                    st.metric("Status", match_info.get("status", "Scheduled"))
            
            if upcoming_match_count == 0:
                st.info("📅 No upcoming matches scheduled.")
            else:
                st.success(f"✅ Found {upcoming_match_count} upcoming matches")
        else:
            st.warning("Unable to fetch upcoming matches from API")
    
    # ===== TAB 3: DATABASE MATCHES =====
    with tab3:
        st.header("📚 Recent Matches from Database")
        
        conn = create_db_connection()
        if not conn:
            st.warning("⚠️ Could not connect to database. Please check your .env configuration.")
            return
        
        try:
            # Get match filters
            col1, col2 = st.columns(2)
            
            with col1:
                # Get unique match formats
                format_query = "SELECT DISTINCT match_format FROM recent_matches WHERE match_format IS NOT NULL ORDER BY match_format"
                formats_df = pd.read_sql(format_query, conn)
                formats = ["All"] + formats_df['match_format'].tolist() if not formats_df.empty else ["All"]
                selected_format = st.selectbox("Match Format", formats)
            
            with col2:
                # Get match states
                state_query = "SELECT DISTINCT state FROM recent_matches WHERE state IS NOT NULL ORDER BY state"
                states_df = pd.read_sql(state_query, conn)
                states = ["All"] + states_df['state'].tolist() if not states_df.empty else ["All"]
                selected_state = st.selectbox("Match State", states)
            
            # Build query based on filters
            query = """
                SELECT 
                    match_id,
                    match_desc,
                    match_format,
                    team1,
                    team2,
                    venue,
                    start_date,
                    state,
                    status
                FROM recent_matches
                WHERE 1=1
            """
            
            params = []
            if selected_format != "All":
                query += " AND match_format = %s"
                params.append(selected_format)
            
            if selected_state != "All":
                query += " AND state = %s"
                params.append(selected_state)
            
            query += " ORDER BY match_id DESC LIMIT 50"
            
            # Execute query
            cursor = conn.cursor()
            cursor.execute(query, params)
            matches = cursor.fetchall()
            
            if not matches:
                st.info("No matches found in database. Add match data via CRUD Operations.")
            else:
                st.success(f"📊 Found {len(matches)} matches in database")
                
                # Display matches
                for match in matches:
                    (match_id, match_desc, match_format, team1, team2, venue, 
                     start_date, state, status) = match
                    
                    with st.expander(f"🏏 {team1} vs {team2} - {match_desc or 'Match'}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("### Match Details")
                            st.write(f"**Match ID:** {match_id}")
                            st.write(f"**Format:** {match_format or 'N/A'}")
                            st.write(f"**Venue:** {venue or 'N/A'}")
                            st.write(f"**Date:** {start_date or 'N/A'}")
                            
                        with col2:
                            st.markdown("### Match Status")
                            st.write(f"**State:** {state or 'N/A'}")
                            st.write(f"**Status:** {status or 'Scheduled'}")
                        
                        # Show batting data for this match if available
                        batting_query = """
                            SELECT player_name, runs, balls_faced, fours, sixes, strike_rate, innings_no
                            FROM batters_bat_data
                            WHERE match_id = %s
                            ORDER BY innings_no, runs DESC
                        """
                        try:
                            batting_df = pd.read_sql(batting_query, conn, params=[match_id])
                            if not batting_df.empty:
                                st.markdown("### 🏏 Batting Performance")
                                st.dataframe(batting_df, use_container_width=True)
                        except:
                            pass
                        
                        # Show bowling data for this match if available
                        bowling_query = """
                            SELECT player_name, overs, runs, wickets, economy_rate, innings_no
                            FROM bowlers_bow_v_data
                            WHERE match_id = %s
                            ORDER BY innings_no, wickets DESC
                        """
                        try:
                            bowling_df = pd.read_sql(bowling_query, conn, params=[match_id])
                            if not bowling_df.empty:
                                st.markdown("### 🎯 Bowling Performance")
                                st.dataframe(bowling_df, use_container_width=True)
                        except:
                            pass
            
            cursor.close()
            
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
