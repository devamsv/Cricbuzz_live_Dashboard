import streamlit as st
import sys
import os

st.set_page_config(page_title="Cricbuzz LiveStats", layout="wide", page_icon="🏏")

# Hide Streamlit's default page navigation
hide_pages_style = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_pages_style, unsafe_allow_html=True)

# Add the pages directory to path for imports
pages_dir = os.path.join(os.path.dirname(__file__), 'pages')
if pages_dir not in sys.path:
    sys.path.insert(0, pages_dir)

# Import page modules
try:
    import importlib.util
    
    spec_home = importlib.util.spec_from_file_location("home", os.path.join(pages_dir, "home.py"))
    home = importlib.util.module_from_spec(spec_home)
    spec_home.loader.exec_module(home)
    
    spec_live = importlib.util.spec_from_file_location("live_matches", os.path.join(pages_dir, "1.live_matches.py"))
    live_matches = importlib.util.module_from_spec(spec_live)
    spec_live.loader.exec_module(live_matches)
    
    spec_stats = importlib.util.spec_from_file_location("top_stats", os.path.join(pages_dir, "2.top_stats.py"))
    top_stats = importlib.util.module_from_spec(spec_stats)
    spec_stats.loader.exec_module(top_stats)
    
    spec_sql = importlib.util.spec_from_file_location("sql_query", os.path.join(pages_dir, "3.sql_query.py"))
    sql_query = importlib.util.module_from_spec(spec_sql)
    spec_sql.loader.exec_module(sql_query)
    
    spec_crud = importlib.util.spec_from_file_location("crud_operations", os.path.join(pages_dir, "4.crud_operations.py"))
    crud_operations = importlib.util.module_from_spec(spec_crud)
    spec_crud.loader.exec_module(crud_operations)
    
except Exception as e:
    st.error(f"Error importing page modules: {e}")
    st.stop()

PAGES = {
    "🏠 Home": home,
    "🏏 Live Scores": live_matches,
    "👤 Player Stats": top_stats,
    "📊 SQL Analytics": sql_query,
    "🛠️ CRUD Operations": crud_operations,
}

with st.sidebar:
    st.title("🏏 Cricket Dashboard")
    st.markdown("### Choose a page:")
    page = st.selectbox("", list(PAGES.keys()), label_visibility="collapsed")
    
    st.markdown("---")
    st.checkbox("Show Debug Info", key="show_debug")

try:
    selected_module = PAGES[page]
    selected_module.app()
except Exception as e:
    st.error(f"Error loading page: {e}")
    st.exception(e)
